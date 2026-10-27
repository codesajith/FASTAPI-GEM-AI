def flatten_skills(*skill_groups: list[str]) -> list[str]:
    """Combine multiple skill lists and remove duplicates."""

    unique_skills = {
        skill
        for group in skill_groups
        for skill in group
    }

    return sorted(unique_skills)


def build_prompt(
    employee_name: str,
    role: str,
    skills: list[str],
    **options
) -> str:
    """Build a reusable AI prompt."""

    skill_text = ", ".join(skills)

    extra_instructions = options.get(
        "instructions",
        "Keep the plan practical and beginner-friendly."
    )

    return (
        f"Create a learning plan for {employee_name}, "
        f"who works as a {role}. "
        f"Current skills: {skill_text}. "
        f"{extra_instructions}"
    )