import pytest
from pyspark.sql import SparkSession
from pyspark_job import clean_data


@pytest.fixture(scope="module")
def spark_local():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("test-customer-orders")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    yield spark

    spark.stop()


COLUMNS = ["order_id", "order_date", "name", "amount"]


def test_valid_records_are_kept(spark_local):
    data = [
        ("1001", "2026-09-01", "Alice", 150.0),
        ("1002", "2026-09-02", "Bob", 20.5),
    ]
    df = spark_local.createDataFrame(data, COLUMNS)

    results = clean_data(df).collect()

    assert len(results) == 2
    assert {r["order_id"] for r in results} == {"1001", "1002"}


def test_amount_less_than_or_equal_zero_removed(spark_local):
    data = [
        ("1001", "2026-09-01", "Alice", 150.0),
        ("1002", "2026-09-02", "Bob", -20.0),
        ("1003", "2026-09-03", "Sara", 0.0),
    ]
    df = spark_local.createDataFrame(data, COLUMNS)

    results = clean_data(df).collect()

    assert len(results) == 1
    assert results[0]["order_id"] == "1001"


def test_null_names_removed(spark_local):
    data = [
        ("1001", "2026-09-01", "Alice", 150.0),
        ("1002", "2026-09-02", None, 80.0),
    ]
    df = spark_local.createDataFrame(data, COLUMNS)

    results = clean_data(df).collect()

    assert len(results) == 1
    assert results[0]["name"] == "Alice"


def test_amount_with_tax_calculated_correctly(spark_local):
    data = [
        ("1001", "2026-09-01", "Alice", 100.0),
        ("1002", "2026-09-02", "Bob", 50.0),
    ]
    df = spark_local.createDataFrame(data, COLUMNS)

    results = clean_data(df).orderBy("order_id").collect()

    assert results[0]["amount_with_tax"] == pytest.approx(120.0)
    assert results[1]["amount_with_tax"] == pytest.approx(60.0)