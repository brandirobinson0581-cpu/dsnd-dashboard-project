from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).resolve().parent
requirements_file = cwd / "employee_events" / "requirements.txt"
requirements = requirements_file.read_text().splitlines()

setup_args = dict(
    name="employee_events",
    version="1.0.0",
    description="SQLite query API for employee performance events",
    packages=find_packages(),
    package_data={"": ["employee_events.db", "requirements.txt"]},
    install_requires=requirements,
    python_requires=">=3.10",
)

if __name__ == "__main__":
    setup(**setup_args)
