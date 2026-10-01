# PySpark CI with GitHub Actions

A small PySpark project that cleans order data and automatically tests the code with GitHub Actions on every push to `main` and every Pull Request targeting `main`.

Built as part of the Samsung Innovation Campus program.

## Description

The project contains a `clean_data(df)` function that takes a Spark DataFrame and:

- Removes rows where `amount <= 0`
- Removes rows where `name` is `NULL`
- Adds a column `amount_with_tax` calculated as `amount * 1.20`

`pyspark_job.py` also includes a `main(csv_path)` entry point that reads a CSV file, applies `clean_data`, and shows the result.

## Project Structure

```
spark-project/
├── .github/
│   └── workflows/
│       └── CI.yaml          # GitHub Actions workflow
├── pyspark_job.py           # clean_data() and main()
├── test_pyspark_job.py      # pytest unit tests
├── requirements.txt         # pyspark==3.5.6, pytest==8.4.2
├── .gitignore
└── README.md
```

## Tests

`test_pyspark_job.py` covers:

1. **Setup:** a module-scoped `spark_local` fixture starts one local Spark session shared by all tests.
2. **Filtering:** valid records are kept, rows with `amount <= 0` are removed, and rows with `NULL` names are removed.
3. **Calculation:** `amount_with_tax` equals `amount * 1.20`.

## Getting Started

**Prerequisites:** Python 3.12 and a JDK (Java 17 recommended), since PySpark runs on the JVM.

```bash
# Create and activate a virtual environment
python3 -m venv dev
source dev/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the tests
python3 -m pytest -v
```

## Run the Job

```bash
python3 pyspark_job.py path/to/orders.csv
```

The CSV must have a header row with at least `name` and `amount` columns.

## Continuous Integration

The workflow in `.github/workflows/CI.yaml` runs on every push to `main` and on every Pull Request targeting `main`. It checks out the code, sets up Java 17 and Python 3.12, installs the dependencies, and runs `pytest`.