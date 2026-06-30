import json
import re


def safe_parse_ai_response(text):
    """
    Safely extracts JSON from an AI response.
    Prevents crashes from malformed model output.
    """

    if not text:
        return {"error": "empty_response"}

    # ----------------------------
    # STEP 1: Try direct JSON parse
    # ----------------------------
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ----------------------------
    # STEP 2: Extract JSON block
    # (handles extra text before/after)
    # ----------------------------
    try:
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
    except json.JSONDecodeError:
        pass

    # ----------------------------
    # STEP 3: Last resort fallback
    # ----------------------------
    return {
        "error": "invalid_ai_response",
        "raw_output": text
    }