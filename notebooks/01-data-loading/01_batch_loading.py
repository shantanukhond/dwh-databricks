# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # 01 — Batch Loading
# MAGIC
# MAGIC 🚧 **Stub** — this is the plan for the lesson. Code is added when the video is recorded.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Plan
# MAGIC
# MAGIC - [ ] Setup: catalog, schema, GHCN source path (NOAA public S3)
# MAGIC - [ ] Full batch load with `spark.read`
# MAGIC - [ ] Incremental load with `COPY INTO`
# MAGIC - [ ] Scheduling discussion
# MAGIC - [ ] Wrap-up & teardown

# COMMAND ----------

import io, pandas as pd

obj = s3.get_object(Bucket="nyc-tlc", Key="misc/taxi_zone_lookup.csv")
pdf = pd.read_csv(io.BytesIO(obj["Body"].read()))
print(pdf.shape)
pdf.head()

# COMMAND ----------

# TODO: full load

# COMMAND ----------

# TODO: incremental load
