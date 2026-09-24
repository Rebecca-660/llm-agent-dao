import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "02_code"))

from run_endpoint_pilot import (
    CANONICAL_OPTION_ORDER,
    CONDITIONS,
    DECODING_REGIMES,
    DEFAULT_DECODING_REGIME,
    PERSONA_IDS,
    RETRY_DELAYS_SECONDS,
    ZHIPU_BASE_URL,
    ZHIPU_DO_SAMPLE,
    ZHIPU_THINKING_MODE,
    api_request_payload,
    build_dry_run_records,
    create_api_client,
    create_execution_run_id,
    decoding_configuration,
    execute_pilot,
    parse_args,
    prepare_execution_paths,
    request_sha256,
    write_dry_run,
)


MODEL = "dry-run-test-model"
OUTPUT_REQUIREMENT_VERSION = "v1.1"
PERSONA_TEMPLATE_VERSION = "v1.1"
REVERSE_OPTION_ORDER = "100%, 75%, 50%, 25%, or 0%"
PLACEHOLDER_PATTERN = re.compile(
    r"(?:\[[A-Za-z][A-Za-z0-9_]*\]|\{[A-Za-z][A-Za-z0-9_]*\})"
)


@pytest.fixture(scope="module")
def records() -> list[dict[str, object]]:
    return build_dry_run_records(
        MODEL, OUTPUT_REQUIREMENT_VERSION, PERSONA_TEMPLATE_VERSION
    )


def test_dry_run_has_exactly_48_unique_balanced_cells(
    records: list[dict[str, object]],
) -> None:
    expected_cells = {
        f"{persona_id}_{condition}"
        for persona_id in PERSONA_IDS
        for condition in CONDITIONS
    }

    assert len(records) == 48
    assert {record["cell_id"] for record in records} == expected_cells
    assert len({record["cell_id"] for record in records}) == 48
    assert Counter(record["persona_id"] for record in records) == Counter(
        {persona_id: 3 for persona_id in PERSONA_IDS}
    )
    assert Counter(record["condition"] for record in records) == Counter(
        {condition: 16 for condition in CONDITIONS}
    )


def test_prompts_are_canonical_complete_and_placeholder_free(
    records: list[dict[str, object]],
) -> None:
    for record in records:
        prompt = str(record["prompt"])
        assert "Kelmoryn Protocol" in prompt
        assert not PLACEHOLDER_PATTERN.findall(prompt)
        assert CANONICAL_OPTION_ORDER in prompt
        assert REVERSE_OPTION_ORDER not in prompt
        assert record["wording_version"] == "canonical_v1.0"
        assert record["persona_template_version"] == "v1.1"
        assert record["persona_template_path"] == (
            "01_prompts/personas/persona_template_v1.1.txt"
        )
        assert "Initiating unstaking starts a 7-day waiting period" in prompt
        assert record["output_requirement_version"] == "v1.1"
        assert record["output_requirement_path"] == (
            "01_prompts/output_schema/json_schema_v1.1.txt"
        )
        assert record["answer_order"] == "canonical_ascending"
        assert '"unstake_percentage": 50' not in prompt


def test_request_metadata_and_hashes_are_complete(
    records: list[dict[str, object]],
) -> None:
    required_fields = {
        "run_id",
        "run_type",
        "run_mode",
        "cell_id",
        "persona_id",
        "condition",
        "provider",
        "api_base_url",
        "sdk_name",
        "openai_sdk_version",
        "decoding_regime",
        "sampling_mode",
        "do_sample",
        "thinking_mode",
        "model",
        "temperature",
        "generated_at",
        "wording_version",
        "persona_template_version",
        "persona_template_path",
        "output_requirement_version",
        "output_requirement_path",
        "answer_order",
        "independent_context",
        "previous_response_id",
        "system_prompt",
        "prompt",
        "system_prompt_sha256",
        "prompt_sha256",
        "request_sha256",
        "source_sha256",
    }

    for record in records:
        assert set(record) == required_fields
        assert record["run_type"] == "pilot"
        assert record["run_mode"] == "dry_run"
        assert record["provider"] == "openai"
        assert record["api_base_url"] == "https://api.openai.com/v1"
        assert record["sdk_name"] == "openai"
        assert record["decoding_regime"] == "greedy_v1.1"
        assert record["sampling_mode"] == "temperature_0"
        assert record["do_sample"] is None
        assert record["thinking_mode"] is None
        assert record["model"] == MODEL
        assert record["temperature"] == 0
        assert record["independent_context"] is True
        assert record["previous_response_id"] is None
        assert hashlib.sha256(str(record["prompt"]).encode()).hexdigest() == record[
            "prompt_sha256"
        ]
        assert (
            hashlib.sha256(str(record["system_prompt"]).encode()).hexdigest()
            == record["system_prompt_sha256"]
        )
        assert request_sha256(
            model=MODEL,
            system_prompt=str(record["system_prompt"]),
            prompt=str(record["prompt"]),
        ) == record["request_sha256"]
        assert len(record["source_sha256"]) == 8
        assert all(
            re.fullmatch(r"[0-9a-f]{64}", digest)
            for digest in record["source_sha256"].values()
        )


def test_write_dry_run_creates_a_zero_call_validation_artifact(
    records: list[dict[str, object]], tmp_path: Path
) -> None:
    output_directory = tmp_path / "pilot_dry_run"
    requests_path, summary_path = write_dry_run(records, output_directory)

    written_records = [
        json.loads(line)
        for line in requests_path.read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert written_records == records
    assert summary["api_calls_made"] == 0
    assert summary["decoding_regime"] == "greedy_v1.1"
    assert summary["persona_template_version"] == "v1.1"
    assert summary["persona_template_path"] == (
        "01_prompts/personas/persona_template_v1.1.txt"
    )
    assert summary["output_requirement_version"] == "v1.1"
    assert summary["output_requirement_path"] == (
        "01_prompts/output_schema/json_schema_v1.1.txt"
    )
    assert summary["record_count"] == 48
    assert summary["unique_cell_count"] == 48
    assert summary["persona_count"] == 16
    assert summary["condition_counts"] == {"S": 16, "C0": 16, "T3": 16}
    assert summary["all_independent_context"] is True

    with pytest.raises(FileExistsError):
        write_dry_run(records, output_directory)


def test_v1_0_and_v1_1_are_explicit_and_reproducible() -> None:
    v1_0_records = build_dry_run_records(MODEL, "v1.0")
    v1_1_records = build_dry_run_records(MODEL, "v1.1")

    assert [record["cell_id"] for record in v1_0_records] == [
        record["cell_id"] for record in v1_1_records
    ]
    for old, new in zip(v1_0_records, v1_1_records, strict=True):
        assert old["output_requirement_version"] == "v1.0"
        assert new["output_requirement_version"] == "v1.1"
        assert old["output_requirement_path"].endswith("json_schema_v1.0.txt")
        assert new["output_requirement_path"].endswith("json_schema_v1.1.txt")
        assert '"unstake_percentage": 50' in old["prompt"]
        assert '"unstake_percentage": 50' not in new["prompt"]
        assert (
            old["source_sha256"][old["output_requirement_path"]]
            != new["source_sha256"][new["output_requirement_path"]]
        )

    for version, first_records in (
        ("v1.0", v1_0_records),
        ("v1.1", v1_1_records),
    ):
        repeated_records = build_dry_run_records(MODEL, version)
        reproducibility_fields = (
            "cell_id",
            "prompt",
            "prompt_sha256",
            "request_sha256",
            "source_sha256",
            "output_requirement_version",
            "output_requirement_path",
        )
        assert [
            {field: record[field] for field in reproducibility_fields}
            for record in first_records
        ] == [
            {field: record[field] for field in reproducibility_fields}
            for record in repeated_records
        ]


def test_persona_v1_0_and_v1_1_are_explicit_and_reproducible() -> None:
    old_records = build_dry_run_records(MODEL, "v1.1", "v1.0")
    new_records = build_dry_run_records(MODEL, "v1.1", "v1.1")
    old_sentence = (
        "Unstaking requires a 7-day waiting period and carries no "
        "additional penalty."
    )
    new_sentences = (
        "Initiating unstaking starts a 7-day waiting period and carries no "
        "additional penalty. Tokens selected for unstaking remain locked "
        "during this period and become unstaked only after the 7-day waiting "
        "period ends."
    )

    assert [record["cell_id"] for record in old_records] == [
        record["cell_id"] for record in new_records
    ]
    for old, new in zip(old_records, new_records, strict=True):
        assert old["persona_template_version"] == "v1.0"
        assert new["persona_template_version"] == "v1.1"
        assert old["persona_template_path"].endswith(
            "persona_template_v1.0.txt"
        )
        assert new["persona_template_path"].endswith(
            "persona_template_v1.1.txt"
        )
        assert old_sentence in old["prompt"]
        assert new_sentences in new["prompt"]
        assert old["prompt"].replace(old_sentence, new_sentences) == new[
            "prompt"
        ]
        assert old["persona_template_path"] in old["source_sha256"]
        assert new["persona_template_path"] in new["source_sha256"]
        assert new["persona_template_path"] not in old["source_sha256"]
        assert old["persona_template_path"] not in new["source_sha256"]

        old_other_hashes = {
            path: digest
            for path, digest in old["source_sha256"].items()
            if path != old["persona_template_path"]
        }
        new_other_hashes = {
            path: digest
            for path, digest in new["source_sha256"].items()
            if path != new["persona_template_path"]
        }
        assert old_other_hashes == new_other_hashes

    repeated = build_dry_run_records(MODEL, "v1.1", "v1.1")
    reproducibility_fields = (
        "cell_id",
        "prompt",
        "prompt_sha256",
        "request_sha256",
        "source_sha256",
        "persona_template_version",
        "persona_template_path",
    )
    assert [
        {field: record[field] for field in reproducibility_fields}
        for record in new_records
    ] == [
        {field: record[field] for field in reproducibility_fields}
        for record in repeated
    ]


def test_unknown_persona_template_version_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown persona template version"):
        build_dry_run_records(MODEL, "v1.1", "v9.9")


def test_unknown_output_requirement_version_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown output requirement version"):
        build_dry_run_records(MODEL, "v9.9")


def test_cli_requires_explicit_output_requirement_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_endpoint_pilot.py",
            "--dry-run",
            "--provider",
            "openai",
            "--model",
            MODEL,
            "--persona-template-version",
            "v1.1",
            "--decoding-regime",
            "greedy_v1.1",
        ],
    )
    with pytest.raises(SystemExit) as error:
        parse_args()
    assert error.value.code == 2


def test_cli_accepts_explicit_v1_1(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_endpoint_pilot.py",
            "--dry-run",
            "--provider",
            "openai",
            "--model",
            MODEL,
            "--persona-template-version",
            "v1.1",
            "--decoding-regime",
            "greedy_v1.1",
            "--output-requirement-version",
            "v1.1",
        ],
    )
    args = parse_args()
    assert args.provider == "openai"
    assert args.decoding_regime == "greedy_v1.1"
    assert args.persona_template_version == "v1.1"
    assert args.output_requirement_version == "v1.1"


def test_cli_requires_explicit_persona_template_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_endpoint_pilot.py",
            "--dry-run",
            "--provider",
            "openai",
            "--model",
            MODEL,
            "--decoding-regime",
            "greedy_v1.1",
            "--output-requirement-version",
            "v1.1",
        ],
    )
    with pytest.raises(SystemExit) as error:
        parse_args()
    assert error.value.code == 2


def test_cli_requires_explicit_decoding_regime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_endpoint_pilot.py",
            "--dry-run",
            "--provider",
            "zhipu",
            "--model",
            "glm-4.7",
            "--persona-template-version",
            "v1.1",
            "--output-requirement-version",
            "v1.1",
        ],
    )
    with pytest.raises(SystemExit) as error:
        parse_args()
    assert error.value.code == 2


def test_cli_accepts_locked_stochastic_regime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_endpoint_pilot.py",
            "--dry-run",
            "--provider",
            "zhipu",
            "--model",
            "glm-4.7",
            "--decoding-regime",
            "stochastic_low_v1.2",
            "--persona-template-version",
            "v1.1",
            "--output-requirement-version",
            "v1.1",
        ],
    )
    args = parse_args()
    assert args.decoding_regime == "stochastic_low_v1.2"


class MockResponse:
    def __init__(self, output_text: str) -> None:
        self.id = "resp_mock"
        self.model = "mock-model-version"
        self.output_text = output_text

    def model_dump(self, mode: str) -> dict[str, object]:
        assert mode == "json"
        return {
            "id": self.id,
            "model": self.model,
            "output_text": self.output_text,
        }


class MockResponses:
    def __init__(self, outcomes: list[object] | None = None) -> None:
        self.outcomes = list(outcomes or ())
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> MockResponse:
        self.calls.append(kwargs)
        outcome = self.outcomes.pop(0) if self.outcomes else MockResponse(
            '{"unstake_percentage": 50, "reason": "Risk remains uncertain."}'
        )
        if isinstance(outcome, Exception):
            raise outcome
        assert isinstance(outcome, MockResponse)
        return outcome


class MockClient:
    def __init__(self, outcomes: list[object] | None = None) -> None:
        self.responses = MockResponses(outcomes)


class MockChatResponse:
    def __init__(self, content: str) -> None:
        self.id = "chatcmpl_mock"
        self.model = "mock-zhipu-model-version"
        self.choices = [
            SimpleNamespace(message=SimpleNamespace(content=content))
        ]
        self._content = content

    def model_dump(self, mode: str) -> dict[str, object]:
        assert mode == "json"
        return {
            "id": self.id,
            "model": self.model,
            "choices": [{"message": {"content": self._content}}],
        }


class MockChatCompletions:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> MockChatResponse:
        self.calls.append(kwargs)
        return MockChatResponse(
            '{"unstake_percentage": 50, "reason": "Risk remains uncertain."}'
        )


class MockZhipuClient:
    def __init__(self) -> None:
        self.chat = SimpleNamespace(completions=MockChatCompletions())


def execution_paths(tmp_path: Path) -> tuple[Path, Path]:
    return prepare_execution_paths(
        "pilot_test_run",
        tmp_path / "raw",
        tmp_path / "logs",
    )


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def test_mock_execution_records_all_48_cells_without_context_chaining(
    records: list[dict[str, object]], tmp_path: Path
) -> None:
    raw_path, attempt_log_path = execution_paths(tmp_path)
    client = MockClient()

    final_records = execute_pilot(
        records,
        client=client,
        run_id="pilot_test_run",
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
        sleep_fn=lambda _: None,
    )

    assert len(final_records) == 48
    assert len(read_jsonl(raw_path)) == 48
    assert len(read_jsonl(attempt_log_path)) == 48
    assert len(client.responses.calls) == 48
    assert all(
        call["previous_response_id"] is None
        for call in client.responses.calls
    )
    assert all(record["status"] == "success" for record in final_records)
    assert all(record["parse_result"]["success"] for record in final_records)
    assert all(record["attempt_count"] == 1 for record in final_records)


def test_zhipu_mock_execution_uses_chat_completions_for_all_48_cells(
    tmp_path: Path,
) -> None:
    zhipu_records = build_dry_run_records(
        "glm-test", OUTPUT_REQUIREMENT_VERSION, provider="zhipu"
    )
    raw_path, attempt_log_path = execution_paths(tmp_path)
    client = MockZhipuClient()

    final_records = execute_pilot(
        zhipu_records,
        client=client,
        run_id="pilot_test_run",
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
        sleep_fn=lambda _: None,
    )

    calls = client.chat.completions.calls
    assert len(calls) == 48
    assert len(final_records) == 48
    assert all(record["provider"] == "zhipu" for record in final_records)
    assert all(record["api_base_url"] == ZHIPU_BASE_URL for record in final_records)
    assert all(
        record["sampling_mode"] == "greedy_do_sample_false"
        for record in final_records
    )
    assert all(record["do_sample"] is False for record in final_records)
    assert all(record["thinking_mode"] == "disabled" for record in final_records)
    assert all(record["status"] == "success" for record in final_records)
    assert all(record["parse_result"]["success"] for record in final_records)
    assert all(
        call["messages"]
        == [
            {"role": "system", "content": record["system_prompt"]},
            {"role": "user", "content": record["prompt"]},
        ]
        for call, record in zip(calls, zhipu_records, strict=True)
    )
    assert all("previous_response_id" not in call for call in calls)
    assert all("instructions" not in call for call in calls)
    assert all(
        call["extra_body"]
        == {
            "do_sample": ZHIPU_DO_SAMPLE,
            "thinking": {"type": ZHIPU_THINKING_MODE},
        }
        for call in calls
    )


def test_locked_stochastic_regime_mock_executes_all_48_cells(
    tmp_path: Path,
) -> None:
    records = build_dry_run_records(
        "glm-4.7",
        "v1.1",
        "v1.1",
        provider="zhipu",
        decoding_regime="stochastic_low_v1.2",
    )
    raw_path, attempt_log_path = execution_paths(tmp_path)
    client = MockZhipuClient()

    final_records = execute_pilot(
        records,
        client=client,
        run_id="pilot_test_run",
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
        sleep_fn=lambda _: None,
    )

    calls = client.chat.completions.calls
    assert len(records) == 48
    assert len({record["cell_id"] for record in records}) == 48
    assert len(calls) == 48
    assert len(final_records) == 48
    assert len(read_jsonl(raw_path)) == 48
    assert len(read_jsonl(attempt_log_path)) == 48
    assert all(record["decoding_regime"] == "stochastic_low_v1.2" for record in records)
    assert all(record["sampling_mode"] == "stochastic_temperature_0.2" for record in records)
    assert all(record["temperature"] == 0.2 for record in records)
    assert all(record["do_sample"] is True for record in records)
    assert all(record["independent_context"] is True for record in records)
    assert all(record["previous_response_id"] is None for record in records)
    assert all(call["temperature"] == 0.2 for call in calls)
    assert all(call["extra_body"]["do_sample"] is True for call in calls)
    assert all(record["status"] == "success" for record in final_records)
    assert all(record["attempt_count"] == 1 for record in final_records)


def test_decoding_regimes_change_only_request_configuration() -> None:
    greedy = build_dry_run_records(
        "glm-4.7",
        "v1.1",
        "v1.1",
        provider="zhipu",
        decoding_regime="greedy_v1.1",
    )
    stochastic = build_dry_run_records(
        "glm-4.7",
        "v1.1",
        "v1.1",
        provider="zhipu",
        decoding_regime="stochastic_low_v1.2",
    )

    assert set(DECODING_REGIMES) == {
        "greedy_v1.1",
        "stochastic_low_v1.2",
    }
    assert DEFAULT_DECODING_REGIME == "greedy_v1.1"
    assert decoding_configuration("greedy_v1.1", "zhipu") == {
        "temperature": 0,
        "do_sample": False,
        "sampling_mode": "greedy_do_sample_false",
    }
    assert decoding_configuration("stochastic_low_v1.2", "zhipu") == {
        "temperature": 0.2,
        "do_sample": True,
        "sampling_mode": "stochastic_temperature_0.2",
    }

    for old, new in zip(greedy, stochastic, strict=True):
        assert old["cell_id"] == new["cell_id"]
        assert old["prompt"] == new["prompt"]
        assert old["system_prompt"] == new["system_prompt"]
        assert old["prompt_sha256"] == new["prompt_sha256"]
        assert old["system_prompt_sha256"] == new["system_prompt_sha256"]
        assert old["source_sha256"] == new["source_sha256"]
        assert old["request_sha256"] != new["request_sha256"]
        assert old["decoding_regime"] == "greedy_v1.1"
        assert new["decoding_regime"] == "stochastic_low_v1.2"
        assert old["temperature"] == 0
        assert new["temperature"] == 0.2
        assert old["do_sample"] is False
        assert new["do_sample"] is True

    repeated = build_dry_run_records(
        "glm-4.7",
        "v1.1",
        "v1.1",
        provider="zhipu",
        decoding_regime="stochastic_low_v1.2",
    )
    stable_fields = (
        "cell_id",
        "prompt",
        "system_prompt",
        "prompt_sha256",
        "system_prompt_sha256",
        "request_sha256",
        "source_sha256",
        "decoding_regime",
        "temperature",
        "do_sample",
    )
    assert [
        {field: record[field] for field in stable_fields}
        for record in stochastic
    ] == [
        {field: record[field] for field in stable_fields}
        for record in repeated
    ]


def test_unknown_or_unsupported_decoding_regime_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown decoding regime"):
        build_dry_run_records(
            "glm-4.7",
            "v1.1",
            "v1.1",
            provider="zhipu",
            decoding_regime="posthoc_best",
        )
    with pytest.raises(ValueError, match="only supported for zhipu"):
        build_dry_run_records(
            MODEL,
            "v1.1",
            "v1.1",
            provider="openai",
            decoding_regime="stochastic_low_v1.2",
        )


def test_provider_specific_request_hashes_and_payloads() -> None:
    openai_records = build_dry_run_records(MODEL, "v1.1", provider="openai")
    zhipu_records = build_dry_run_records(MODEL, "v1.1", provider="zhipu")

    assert [record["prompt_sha256"] for record in openai_records] == [
        record["prompt_sha256"] for record in zhipu_records
    ]
    assert all(
        old["request_sha256"] != new["request_sha256"]
        for old, new in zip(openai_records, zhipu_records, strict=True)
    )
    payload = api_request_payload(
        provider="zhipu",
        model=MODEL,
        system_prompt="system",
        prompt="prompt",
    )
    assert payload["messages"] == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "prompt"},
    ]
    assert payload["temperature"] == 0
    assert payload["extra_body"] == {
        "do_sample": False,
        "thinking": {"type": "disabled"},
    }


def test_transient_error_is_retried_and_every_attempt_is_logged(
    records: list[dict[str, object]], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    class MockTransientError(Exception):
        pass

    import run_endpoint_pilot

    monkeypatch.setattr(
        run_endpoint_pilot, "TRANSIENT_ERROR_TYPES", (MockTransientError,)
    )
    raw_path, attempt_log_path = execution_paths(tmp_path)
    client = MockClient(
        [
            MockTransientError("temporary failure"),
            MockResponse(
                '{"unstake_percentage": 25, "reason": "Risk remains."}'
            ),
        ]
    )
    delays: list[float] = []

    final_records = execute_pilot(
        records,
        client=client,
        run_id="pilot_test_run",
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
        sleep_fn=delays.append,
    )
    attempts = read_jsonl(attempt_log_path)

    assert len(final_records) == 48
    assert len(client.responses.calls) == 49
    assert len(attempts) == 49
    assert final_records[0]["attempt_count"] == 2
    assert attempts[0]["status"] == "api_error"
    assert attempts[0]["transient_error"] is True
    assert attempts[0]["retry_scheduled"] is True
    assert attempts[1]["status"] == "response_received"
    assert delays == [RETRY_DELAYS_SECONDS[0]]


def test_invalid_model_content_is_saved_without_retry(
    records: list[dict[str, object]], tmp_path: Path
) -> None:
    raw_path, attempt_log_path = execution_paths(tmp_path)
    client = MockClient([MockResponse("not valid JSON")])

    final_records = execute_pilot(
        records,
        client=client,
        run_id="pilot_test_run",
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
        sleep_fn=lambda _: None,
    )

    assert len(client.responses.calls) == 48
    assert len(final_records) == 48
    assert final_records[0]["status"] == "success"
    assert final_records[0]["attempt_count"] == 1
    assert final_records[0]["parse_result"]["success"] is False
    assert len(read_jsonl(attempt_log_path)) == 48


def test_non_transient_error_is_not_retried(
    records: list[dict[str, object]], tmp_path: Path
) -> None:
    raw_path, attempt_log_path = execution_paths(tmp_path)
    client = MockClient([ValueError("permanent failure")])

    final_records = execute_pilot(
        records,
        client=client,
        run_id="pilot_test_run",
        raw_path=raw_path,
        attempt_log_path=attempt_log_path,
        sleep_fn=lambda _: None,
    )

    assert len(client.responses.calls) == 48
    assert len(final_records) == 48
    assert final_records[0]["status"] == "api_error"
    assert final_records[0]["attempt_count"] == 1
    assert final_records[0]["parse_result"] is None
    assert len(read_jsonl(attempt_log_path)) == 48


def test_execution_output_paths_are_exclusive(tmp_path: Path) -> None:
    execution_paths(tmp_path)
    with pytest.raises(FileExistsError):
        execution_paths(tmp_path)


def test_each_execution_run_id_is_new() -> None:
    first = create_execution_run_id()
    second = create_execution_run_id()

    assert first.startswith("pilot_")
    assert second.startswith("pilot_")
    assert first != second


def test_openai_client_disables_unlogged_sdk_retries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import run_endpoint_pilot

    captured: dict[str, object] = {}

    def fake_openai(**kwargs: object) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(run_endpoint_pilot, "OpenAI", fake_openai)

    assert create_api_client("openai") is not None
    assert captured == {"max_retries": 0}


def test_zhipu_client_uses_separate_key_and_fixed_base_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import run_endpoint_pilot

    captured: dict[str, object] = {}

    def fake_openai(**kwargs: object) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(run_endpoint_pilot, "OpenAI", fake_openai)
    monkeypatch.setenv("ZAI_API_KEY", "test-only-zhipu-key")

    assert create_api_client("zhipu") is not None
    assert captured == {
        "api_key": "test-only-zhipu-key",
        "base_url": ZHIPU_BASE_URL,
        "max_retries": 0,
    }


def test_zhipu_client_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ZAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="ZAI_API_KEY"):
        create_api_client("zhipu")
