from database.db import get_connection
import json


def apply_ai_adjustment(user_id, ai_response):
    """
    Applies AI decision to stored plan and updates versioning.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # 1. FETCH CURRENT PLAN
    cursor.execute(
        "SELECT * FROM plans WHERE user_id = ?",
        (user_id,)
    )

    row = cursor.fetchone()

    if not row:
        conn.close()
        return None

    plan = dict(row)

    # 2. SAFE DECISION EXTRACTION
    decision = "keep"

    if isinstance(ai_response, dict):
        decision = ai_response.get("decision", "keep")

    # 3. KEEP PLAN (NO CHANGE)
    if decision == "keep":
        conn.close()
        return plan

    # 4. INCREMENT VERSION
    new_version = (plan.get("version") or 1) + 1

    # 5. UPDATE PLAN METADATA ONLY (MVP SAFE APPROACH)
    updated_plan = {
        "content": plan["content"],
        "version": new_version,
        "last_decision": decision,
        "last_update": json.dumps(ai_response),
    }

    # 6. SAVE BACK TO DB
    cursor.execute("""
        UPDATE plans
        SET content = ?,
            version = ?,
            created_at = ?
        WHERE user_id = ?
    """, (
        updated_plan["content"],
        updated_plan["version"],
        plan["created_at"],  # keep original timestamp
        user_id
    ))

    conn.commit()
    conn.close()

    return updated_plan