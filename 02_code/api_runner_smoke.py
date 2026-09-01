import json
from pathlib import Path
from datetime import datetime
from openai import OpenAI

MODEL = "gpt-4o-mini"
TEMPERATURE = 0
PROMPT_FILE = Path("validation/P01_all_arms/P01_T3.txt")
OUTPUT_DIR = Path("03_raw_outputs/smoke")

client = OpenAI()

def main():
    print("Script started.")
    print(f"Reading prompt file: {PROMPT_FILE}")
    if not PROMPT_FILE.exists():
        print(f"Error: file not found - {PROMPT_FILE}")
        return
    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
    print(f"Prompt loaded, length: {len(prompt_text)}")
    messages = [
        {"role": "system", "content": "You are an AI assistant. Return your response in valid JSON format."},
        {"role": "user", "content": prompt_text}
    ]
    print("Calling API (timeout 30s)...")
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            timeout=30.0,
            response_format={"type": "json_object"}
        )
    except Exception as e:
        print(f"API call failed: {e}")
        return
    raw_content = response.choices[0].message.content
    print("Response received:")
    print(raw_content)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"run_smoke_t3_{timestamp}.jsonl"
    record = {
        "run_id": f"smoke_t3_{timestamp}",
        "model": MODEL,
        "temperature": TEMPERATURE,
        "timestamp": timestamp,
        "prompt_file": str(PROMPT_FILE),
        "raw_output": raw_content
    }
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Result saved to: {output_file}")

if __name__ == "__main__":
    main()