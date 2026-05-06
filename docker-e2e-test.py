import json
import urllib.error
import urllib.request

BACKEND_URL = "http://localhost:8080/api/ai/prompt"
TEST_PROMPT = "E2E check: verify AI integration through backend."


def post_prompt(prompt: str) -> dict:
    payload = json.dumps({"prompt": prompt}).encode("utf-8")
    request = urllib.request.Request(
        BACKEND_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


if __name__ == "__main__":
    try:
        result = post_prompt(TEST_PROMPT)
        print("E2E test passed. Backend->AI response:")
        print(json.dumps(result, indent=2))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        print(f"E2E test failed with HTTP {exc.code}: {body}")
        raise
    except Exception as exc:
        print(f"E2E test failed: {exc}")
        raise
