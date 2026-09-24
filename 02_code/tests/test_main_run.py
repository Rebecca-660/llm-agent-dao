import json
import sys
from collections import Counter
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "02_code"))

import run_main_run as main


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeChoice:
    def __init__(self, content):
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content, number=1):
        self.id = f"response-{number}"
        self.model = "glm-4.7"
        self.choices = [FakeChoice(content)]

    def model_dump(self, mode="json"):
        return {"id": self.id, "model": self.model, "mode": mode}


class FakeCompletions:
    def __init__(self, outcomes=None, default_content=None):
        self.outcomes = list(outcomes or [])
        self.default_content = default_content or '{"unstake_percentage": 25, "reason": "A concise reason."}'
        self.calls = []

    def create(self, **payload):
        self.calls.append(payload)
        outcome = self.outcomes.pop(0) if self.outcomes else self.default_content
        if isinstance(outcome, Exception):
            raise outcome
        return FakeResponse(outcome, len(self.calls))


class FakeChat:
    def __init__(self, completions):
        self.completions = completions


class FakeClient:
    def __init__(self, outcomes=None, default_content=None):
        self.completions = FakeCompletions(outcomes, default_content)
        self.chat = FakeChat(self.completions)


def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def records():
    return main.build_main_request_records()


def execution_paths(tmp_path, run_id="main_20260904T000000Z_test0001"):
    return main.prepare_execution_paths(run_id, tmp_path / "raw", tmp_path / "logs")


def test_frozen_hashes_verify_and_cover_all_expected_files():
    hashes = main.verify_frozen_hashes()
    assert set(hashes) == set(main.FROZEN_FILE_PATHS)
    assert all(len(value) == 64 for value in hashes.values())


def test_frozen_hash_mismatch_stops_before_request_build(monkeypatch):
    monkeypatch.setattr(main.shared, "sha256_file", lambda path: "0" * 64)
    with pytest.raises(RuntimeError, match="Frozen file hash mismatch"):
        main.build_main_request_records()


@pytest.mark.parametrize(
    "override",
    [
        {"provider": "openai"}, {"model": "glm-5"},
        {"decoding_regime": "greedy_v1.1"},
        {"persona_template_version": "v1.0"},
        {"output_requirement_version": "v1.0"},
        {"answer_order": "reverse"},
    ],
)
def test_nonfrozen_selection_is_rejected(override):
    with pytest.raises(ValueError, match="must match freeze"):
        main.build_main_request_records(**override)


def test_builds_exact_complete_five_arm_matrix(records):
    assert len(records) == 80
    assert len({record["cell_id"] for record in records}) == 80
    assert Counter(record["condition"] for record in records) == Counter({arm: 16 for arm in main.CONDITIONS})
    assert {record["persona_id"] for record in records} == set(main.PERSONA_IDS)


def test_every_record_has_frozen_configuration_and_independent_context(records):
    for record in records:
        assert record["run_type"] == "main"
        assert record["provider"] == "zhipu"
        assert record["model"] == "glm-4.7"
        assert record["decoding_regime"] == "stochastic_low_v1.2"
        assert record["do_sample"] is True
        assert record["temperature"] == 0.2
        assert record["thinking_mode"] == "disabled"
        assert record["persona_template_version"] == "v1.1"
        assert record["output_requirement_version"] == "v1.1"
        assert record["answer_order"] == "canonical_ascending"
        assert record["independent_context"] is True
        assert record["previous_response_id"] is None


def test_hash_and_metadata_fields_are_complete_and_no_placeholders(records):
    for record in records:
        assert len(record["prompt_sha256"]) == 64
        assert len(record["system_prompt_sha256"]) == 64
        assert len(record["request_sha256"]) == 64
        assert len(record["freeze_record_sha256"]) == 64
        assert record["main_runner_path"] == "02_code/run_main_run.py"
        assert record["main_runner_sha256"] == main.shared.sha256_file(main.MAIN_RUNNER_PATH)
        assert record["source_sha256"]
        assert record["verified_frozen_sha256"]
        assert not main.UNRESOLVED_PLACEHOLDER_PATTERN.search(record["prompt"])
        assert not main.UNRESOLVED_PLACEHOLDER_PATTERN.search(record["system_prompt"])


def test_main_run_ids_are_new_and_never_pilot_ids():
    first = main.create_execution_run_id()
    second = main.create_execution_run_id()
    assert first.startswith("main_") and second.startswith("main_")
    assert "pilot" not in first.lower()
    assert first != second


def test_prepare_paths_is_exclusive_and_rejects_pilot_identity(tmp_path):
    run_id = "main_20260904T000000Z_test0002"
    raw, log = execution_paths(tmp_path, run_id)
    assert raw.exists() and log.exists()
    with pytest.raises(FileExistsError):
        execution_paths(tmp_path, run_id)
    with pytest.raises(ValueError, match="main_ run ID"):
        execution_paths(tmp_path, "pilot_20260904_bad")


def test_successful_mock_execution_records_all_80_cells(records, tmp_path):
    raw, log = execution_paths(tmp_path, "main_20260904T000000Z_success1")
    client = FakeClient()
    final = main.execute_main(records, client=client, run_id="main_20260904T000000Z_success1", raw_path=raw, attempt_log_path=log, sleep_fn=lambda delay: None)
    assert len(final) == 80
    assert len(client.completions.calls) == 80
    assert len(jsonl(raw)) == 80
    assert len(jsonl(log)) == 80
    assert all(record["run_type"] == "main" for record in jsonl(raw) + jsonl(log))
    assert all(record["parse_result"]["success"] for record in final)


def test_transient_error_retries_by_fixed_rule(monkeypatch, records, tmp_path):
    class TemporaryError(Exception):
        pass

    raw, log = execution_paths(tmp_path, "main_20260904T000000Z_retry001")
    client = FakeClient(outcomes=[TemporaryError("temporary")])
    sleeps = []
    monkeypatch.setattr(main, "is_transient_error", lambda error: isinstance(error, TemporaryError))
    final = main.execute_main(records, client=client, run_id="main_20260904T000000Z_retry001", raw_path=raw, attempt_log_path=log, sleep_fn=sleeps.append)
    attempts = jsonl(log)
    assert len(client.completions.calls) == 81
    assert len(attempts) == 81
    assert sleeps == [1.0]
    assert final[0]["attempt_count"] == 2
    assert attempts[0]["retry_scheduled"] is True


def test_nontransient_api_failure_is_recorded_without_retry(monkeypatch, records, tmp_path):
    raw, log = execution_paths(tmp_path, "main_20260904T000000Z_failure1")
    client = FakeClient(default_content=ValueError("permanent"))
    monkeypatch.setattr(main, "is_transient_error", lambda error: False)
    final = main.execute_main(records, client=client, run_id="main_20260904T000000Z_failure1", raw_path=raw, attempt_log_path=log, sleep_fn=lambda delay: None)
    assert len(client.completions.calls) == 80
    assert len(jsonl(log)) == 80
    assert all(record["status"] == "api_error" for record in final)
    assert all(record["attempt_count"] == 1 for record in final)


def test_invalid_successful_content_is_not_reasked(records, tmp_path):
    raw, log = execution_paths(tmp_path, "main_20260904T000000Z_invalid1")
    client = FakeClient(outcomes=['{"unstake_percentage": 30, "reason": "Invalid value."}'])
    final = main.execute_main(records, client=client, run_id="main_20260904T000000Z_invalid1", raw_path=raw, attempt_log_path=log, sleep_fn=lambda delay: None)
    assert len(client.completions.calls) == 80
    assert len(jsonl(log)) == 80
    assert final[0]["status"] == "success"
    assert final[0]["parse_result"]["success"] is False
    assert final[0]["attempt_count"] == 1


def test_dry_run_writer_is_zero_api_and_refuses_overwrite(records, tmp_path):
    output = tmp_path / "dry"
    request_path, summary_path = main.write_dry_run(records, output)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert len(jsonl(request_path)) == 80
    assert summary["api_calls_made"] == 0
    assert summary["run_type"] == "main"
    assert summary["condition_counts"] == {arm: 16 for arm in main.CONDITIONS}
    with pytest.raises(FileExistsError):
        main.write_dry_run(records, output)
