import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def clean_data(df):
    """
    clean_data Function take a spark datafram apply this transformation 
        • Remove rows where amount <= 0. 
        • Remove rows where name is NULL. 
        • Add a column amount_with_tax. 
        • Calculate amount_with_tax as amount * 1.20. 
    """
    return (
           df
           .filter(col("amount") > 0)
           .na.drop(subset=["name"])
           .withColumn("amount_with_tax", col("amount") * 1.20)
       )


def main(csv_path):
    spark = (
        SparkSession.builder
        .appName("CustomerOrderCleaning")
        .getOrCreate()
    )

    try:
        # Read the CSV file.
        # Example path:
        # hdfs:///data/customer_orders.csv
        df = (
            spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .option("mode", "PERMISSIVE")
            .csv(csv_path)
        )

        # Apply cleaning transformations.
        cleaned = clean_data(df)

        # Show the cleaned orders in the Spark output/logs.
        cleaned.show(truncate=False)

        # Optional: write the cleaned data as CSV.
        # Note: Spark writes a folder containing one or more CSV part files.
        #
        # (
        #     cleaned.write
        #     .mode("overwrite")
        #     .option("header", "true")
        #     .csv("hdfs:///data/cleaned_customer_orders")
        # )

        return cleaned

    finally:
        spark.stop()


if __name__ == "__main__":
    main(sys.argv[1])