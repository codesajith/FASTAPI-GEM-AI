import json
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "employees.json"
)


def load_employees() -> list[dict]:
    """Read employees from the JSON file."""

    with DATA_FILE.open("r", encoding="utf-8") as file:
        employees = json.load(file)

    return employees


def get_employee(employee_id: int) -> dict | None:
    """Return an employee or None if not found."""

    employees = load_employees()

    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


def search_employees(skill: str) -> list[dict]:
    """Find employees with a matching skill."""

    employees = load_employees()
    search_term = skill.casefold()

    return [
        employee
        for employee in employees
        if any(
            item.casefold() == search_term
            for item in employee["skills"]
        )
    ]