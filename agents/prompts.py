SYSTEM_PROMPTS = {
    # framing_A2: original expert role + style constraint appended; beginner unchanged
    "expert": """
Reply ONLY in Markdown using the response format in the task. No extra text before or after.
List each finding as a single bullet point. One sentence per finding. No elaboration.
""",
    "beginner": """
Reply ONLY in Markdown using the response format in the task. No extra text before or after.
""",
}
