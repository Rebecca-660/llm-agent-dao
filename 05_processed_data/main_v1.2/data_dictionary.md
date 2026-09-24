# Main v1.2 processed-data dictionary

Each row represents one planned persona × treatment cell from the single authorized main run. The dataset contains all 80 planned cells, including invalid observations retained as missing.

| Field | Meaning |
|---|---|
| `run_id`, `run_type` | Authorized run identity and `main` classification. |
| `cell_id` | Unique `persona_id` + treatment-arm key. |
| `persona_id`, `condition` | Frozen persona ID and one of `S/C0/T1/T2/T3`. |
| `raw_line_number` | One-based locator in the authorized raw JSONL. |
| `raw_record_sha256` | SHA-256 of the exact UTF-8 JSONL line without its line ending. |
| `request_sha256`, `prompt_sha256`, `system_prompt_sha256` | Recorded request provenance hashes. |
| `response_id` | Provider response identifier, when received. |
| `api_status`, `attempt_count` | Final API status and number of recorded attempts. |
| `outcome_status` | `valid`, `parse_failure`, `illegal_value`, `empty_response`, `refusal`, or `api_error`. |
| `parse_success`, `parse_error` | Frozen-parser result and verbatim error message. |
| `unstake_percentage` | Parsed legal outcome for valid records; missing otherwise. |
| `any_unstake` | `1` for a valid percentage above zero and `0` for a valid zero; missing for every invalid record. |
| `reason` | Parsed non-empty reason for valid records; missing otherwise. |

Missing values are serialized as empty cells in CSV and `null` in JSONL. They are never treated as zero. The raw response itself is not duplicated in the processed dataset; it remains immutable in the raw JSONL and is traceable by run ID, line number, record hash, and response ID.
