from database.db import get_connection
import json
from services.plan_merge_service import merge_plan_changes


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
        plan["content"] = json.loads(plan["content"])
        conn.close()
        return plan

    # 4. LOAD CURRENT PLAN
    current_plan = json.loads(plan["content"])

    # 5. GET AI WORKOUT CHANGES
    workout_changes = {}

    if isinstance(ai_response, dict):
        workout_changes = ai_response.get("workout_changes", {})

    # 6. MERGE CHANGES INTO PLAN
    updated_content = merge_plan_changes(
        current_plan,
        workout_changes
    )

    # 7. INCREMENT VERSION
    new_version = (plan["version"] or 1) + 1

    # 8. SAVE UPDATED PLAN
    cursor.execute("""
        UPDATE plans
        SET content = ?,
            version = ?,
            created_at = ?
        WHERE user_id = ?
    """, (
        json.dumps(updated_content),
        new_version,
        plan["created_at"],
        user_id
    ))

    conn.commit()
    conn.close()

    return {
        "version": new_version,
        "decision": decision,
        "content": updated_content
    }