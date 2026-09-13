# Employee Performance Dashboard

[![Tests](https://github.com/brandirobinson0581-cpu/dsnd-dashboard-project/actions/workflows/test.yml/badge.svg)](https://github.com/brandirobinson0581-cpu/dsnd-dashboard-project/actions/workflows/test.yml)
[![Lint](https://github.com/brandirobinson0581-cpu/dsnd-dashboard-project/actions/workflows/lint.yml/badge.svg)](https://github.com/brandirobinson0581-cpu/dsnd-dashboard-project/actions/workflows/lint.yml)

This project turns employee performance-event data into an interactive dashboard for manufacturing managers. It combines a reusable SQLite query package, object-oriented FastHTML components, two data visualizations, and an existing recruitment-risk model.

Managers can switch between employee and team views to review cumulative positive and negative events, performance notes, and predicted recruitment risk. The risk chart uses green, amber, and red to make lower, medium, and higher probabilities easy to distinguish.

## Features

- Employee and team selectors backed by SQLite queries
- Dynamic **Employee Performance** and **Team Performance** headings
- Cumulative positive/negative event visualization
- Recruitment-risk visualization using the supplied model
- Team risk calculated as the mean of member-level probabilities
- Performance notes table for the selected employee or team
- Reusable Python package and object-oriented dashboard components
- Automated tests and linting through GitHub Actions

## Repository structure

```text
assets/                 Model and dashboard stylesheet
python-package/         Installable employee_events package
  dist/                 Source distribution (.tar.gz)
report/                 FastHTML dashboard and UI components
tests/                  Database, query, and dashboard tests
.github/workflows/      Push and pull-request automation
requirements.txt        Reproducible project environment
```

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The root requirements file installs the local `employee_events` package in editable mode. To build the required source distribution separately:

```bash
cd python-package
python setup.py sdist
cd ..
```

## Run the dashboard

```bash
python report/dashboard.py
```

Open the local address printed by FastHTML (normally `http://localhost:5001`). The home page defaults to an employee view. Direct routes are also available:

- `/employee/<employee_id>`
- `/team/<team_id>`

## Test and lint

```bash
pytest -q
flake8 python-package report tests
```

The test workflow runs automatically on every push to `main` and on pull requests targeting `main`.

## Design

`QueryMixin` owns connection and execution behavior, while `QueryBase` defines shared entity queries. `Employee` and `Team` inherit from that base and provide entity-specific SQL. In the dashboard, small base components handle tables, selectors, and Matplotlib rendering; combined components compose them into the final report. This keeps SQL, visualization, and page-layout responsibilities separate.

The recruitment model uses total positive and negative event counts. Predictions should support manager review rather than make employment decisions automatically.
