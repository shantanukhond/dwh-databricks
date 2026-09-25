---
title: Type 0 · Fixed
---

import YouTube from '@site/src/components/YouTube';

<YouTube id="dRDkECxAJyY" title="SCD Type 0 demo" />

Type 0 slowly changing dimensions (SCDs) keep the original value of a
dimension record. When a source record changes, the new value is ignored and
the first value remains unchanged.

The clearest full-table example is a calendar dimension. Once dates and their
fiscal or holiday classifications are published, reports should continue to
use the same definitions. New future dates can be added, but existing dates
are not overwritten.

## Dimension shape

The dimension keeps one row per calendar date. There are no effective dates or
previous-value columns because the original reference values are the only
values retained:

```sql
CREATE OR REPLACE TABLE sandbox.bronze.dim_calendar (
	id BIGINT GENERATED ALWAYS AS IDENTITY,
	calendar_date DATE,
	calendar_year INT,
	fiscal_year INT,
	fiscal_quarter INT,
	month_number INT,
	month_name STRING,
	day_of_month INT,
	day_of_week_number INT,
	day_of_week_name STRING,
	is_weekend BOOLEAN,
	is_holiday BOOLEAN,
	loaded_at TIMESTAMP
) USING DELTA;
```

If a holiday classification is corrected later, that correction is intentionally
not applied to this Type 0 table. Handle it as a new published calendar
version if the business needs to preserve both definitions.

## Create and populate one year

The following scripts create `sandbox.ingress.dim_calendar` and populate one
calendar year. Change `calendar_year` to load a different year.

### SQL

```sql
DECLARE OR REPLACE VARIABLE CALENDAR_YEAR INT DEFAULT 2025;

CREATE TABLE IF NOT EXISTS sandbox.ingress.dim_calendar (
	calendar_date DATE,
	calendar_year INT,
	fiscal_year INT,
	fiscal_quarter INT,
	month_number INT,
	month_name STRING,
	day_of_month INT,
	day_of_week_number INT,
	day_of_week_name STRING,
	is_weekend BOOLEAN,
	is_holiday BOOLEAN,
	loaded_at TIMESTAMP
) USING DELTA;

INSERT INTO sandbox.ingress.dim_calendar
SELECT
	calendar_date,
	year(calendar_date) AS calendar_year,
	year(calendar_date) AS fiscal_year,
	quarter(calendar_date) AS fiscal_quarter,
	month(calendar_date) AS month_number,
	date_format(calendar_date, 'MMMM') AS month_name,
	day(calendar_date) AS day_of_month,
	dayofweek(calendar_date) AS day_of_week_number,
	date_format(calendar_date, 'EEEE') AS day_of_week_name,
	dayofweek(calendar_date) IN (1, 7) AS is_weekend,
	false AS is_holiday,
	current_timestamp() AS loaded_at
FROM (
	SELECT explode(
		sequence(
			make_date(calendar_year, 1, 1),
			make_date(calendar_year, 12, 31),
			interval 1 day
		)
	) AS calendar_date
);
```

The SQL script uses the calendar year as the parameter and generates every date
from January 1 through December 31, including leap-day dates when applicable.
The `is_holiday` column is initialized to `false`; populate the applicable
holiday dates before publishing the Type 0 calendar.

### PySpark

```python
from datetime import date

from pyspark.sql import functions as F

calendar_year = 2026
table_name = "sandbox.ingress.dim_calendar"

start_date = date(calendar_year, 1, 1)
end_date = date(calendar_year, 12, 31)

calendar_df = (
	spark.range(1)
	.select(
		F.explode(
			F.sequence(
				F.lit(start_date),
				F.lit(end_date),
				F.expr("INTERVAL 1 DAY"),
			)
		).alias("calendar_date")
	)
	.select(
		"calendar_date",
		F.year("calendar_date").alias("calendar_year"),
		F.year("calendar_date").alias("fiscal_year"),
		F.quarter("calendar_date").alias("fiscal_quarter"),
		F.month("calendar_date").alias("month_number"),
		F.date_format("calendar_date", "MMMM").alias("month_name"),
		F.dayofmonth("calendar_date").alias("day_of_month"),
		F.dayofweek("calendar_date").alias("day_of_week_number"),
		F.date_format("calendar_date", "EEEE").alias("day_of_week_name"),
		F.dayofweek("calendar_date").isin([1, 7]).alias("is_weekend"),
		F.lit(False).alias("is_holiday"),
		F.current_timestamp().alias("loaded_at"),
	)
)

calendar_df.write.format("delta").mode("append").saveAsTable(table_name)
```

Use `mode("append")` only when loading a year that is not already present.
Because this is a Type 0 table, do not overwrite existing dates with a later
source version.

## Process
We can handle the Type 0 load with one simple Delta `MERGE`. Since the merge
matches records on `calendar_date`, existing dates are left unchanged and only
new dates are inserted.

```python
from delta.tables import DeltaTable
from pyspark.sql.functions import col

ing_cal_df = DeltaTable.forName(spark, "sandbox.ingress.dim_calendar").toDF()

brz_cal = DeltaTable.forName(spark, "sandbox.bronze.dim_calendar")

brz_cal.alias("brz").merge(
	ing_cal_df.alias("ing"),
	col("brz.calendar_date") == col("ing.calendar_date")
).whenNotMatchedInsertAll().execute()
```

There is no `whenMatchedUpdate` clause because Type 0 does not update an
existing date. Running the merge again is safe as long as `calendar_date` is
unique in the ingress table. The notebook checks the number of records after
the merge:

```python
DeltaTable.forName(spark, "sandbox.bronze.dim_calendar").toDF().count()
```

To reset the bronze table before rerunning the demo:

```sql
TRUNCATE TABLE sandbox.bronze.dim_calendar;
```

## Type 0 versus Type 1

| Requirement | Type 0 | Type 1 |
|---|---|---|
| Existing record changes | Ignore the change | Overwrite the old value |
| History retained | Original value | Latest value |
| Best for | Immutable attributes | Current-state reporting |

## Try it

Load an initial calendar in ingress and run the merge. Then correct the holiday
flag for an existing date and add a new future date. Run the merge again. The
existing date keeps its original flag, while the new date is inserted.
