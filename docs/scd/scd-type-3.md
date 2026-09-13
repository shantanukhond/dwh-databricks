---
title: Type 3 · Previous Value
---

Type 3 slowly changing dimensions (SCDs) keep the current value and one
previous value in the same dimension row. When a customer changes address, the
current address moves to the previous-address column and the incoming address
becomes the current value.

This pattern is useful when reports only need to compare the value now with the
value immediately before it. Unlike Type 2, it does not retain every version
of the record.

## Dimension shape

The dimension keeps one row per business key. Each tracked attribute has a
current and previous column:

```sql
CREATE OR REPLACE TABLE sandbox.bronze.customer (
	id BIGINT GENERATED ALWAYS AS IDENTITY,
	c_custkey BIGINT,
	c_address_current STRING,
	c_address_previous STRING,
	last_updated_at TIMESTAMP,
	is_active BOOLEAN
) USING DELTA;
```

For a new customer, the current columns receive the incoming values and the
previous columns are `NULL`. For an update, the old current values are copied
to their matching previous columns and the incoming values become current.
`is_active` is `true` for an active customer.

## Process

For this demo, the source only needs the business key and the address:
`c_custkey` and `c_address`.

### 1. Identify new records

Use a left anti join to find customers that exist in the ingress data but not
in the Type 3 dimension. The previous columns start as `NULL`.

```python
from datetime import datetime

from pyspark.sql.functions import col, lit

new_df = ing_df.alias("ing").join(
	brz_df.alias("brz"),
	col("ing.c_custkey") == col("brz.c_custkey"),
	"leftanti",
).select("ing.*").withColumns({
	"c_address_current": col("c_address"),
	"c_address_previous": lit(None).cast("string"),
	"last_updated_at": lit(datetime.now()),
	"is_active": lit(True),
})

display(new_df)
```

### 2. Identify updated records

Join ingress to the active dimension row and compare the source attributes
with their current counterparts. The changed current values are copied into
the matching previous columns before the incoming values replace them.

```python
updated_df = ing_df.alias("ing").join(
	brz_df.alias("brz"),
	(col("ing.c_custkey") == col("brz.c_custkey"))
	& col("brz.is_active"),
	"inner",
).filter(
	col("ing.c_address") != col("brz.c_address_current")
).select(
	col("ing.c_custkey"),
	col("ing.c_address").alias("c_address_current"),
	col("brz.c_address_current").alias("c_address_previous"),
).withColumns({
	"last_updated_at": lit(datetime.now()),
	"is_active": lit(True),
})

display(updated_df)
```

This intentionally keeps only one previous value. If the address changes a
second time, the first address is overwritten by the immediately preceding
address.

### 3. Identify deleted records

Type 3 does not need a new row for a deleted customer. Find dimension rows that
are missing from ingress and mark them inactive. Keeping the last current and
previous values makes the row available for auditing without treating it as an
active customer.

```python
deleted_df = brz_df.alias("brz").join(
	ing_df.alias("ing"),
	col("brz.c_custkey") == col("ing.c_custkey"),
	"leftanti",
).filter(col("brz.is_active"))

deleted_df = deleted_df.withColumn("last_updated_at", lit(datetime.now())) \
	.withColumn("is_active", lit(False))

display(deleted_df)
```

### 4. Merge the changes

The three result sets can be applied to the dimension with one Delta Lake
`MERGE`. New records are inserted, updated records replace the current and
previous columns, and deleted records are marked inactive.

```python
from delta.tables import DeltaTable

customer_dim = DeltaTable.forName(spark, "sandbox.bronze.customer")

customer_dim.alias("brz").merge(
	updated_df.unionByName(new_df, allowMissingColumns=True)
		.unionByName(deleted_df, allowMissingColumns=True)
		.alias("changes"),
	"brz.c_custkey = changes.c_custkey",
).whenMatchedUpdate(
	condition="changes.is_active = false",
	set={
		"is_active": "changes.is_active",
		"last_updated_at": "changes.last_updated_at",
	},
).whenMatchedUpdate(
	condition="changes.is_active = true",
	set={
		"c_address_current": "changes.c_address_current",
		"c_address_previous": "changes.c_address_previous",
		"last_updated_at": "changes.last_updated_at",
		"is_active": "changes.is_active",
	},
).whenNotMatchedInsertAll().execute()
```

In production, build the change sets so that each business key appears only
once in the merge source. Delta Lake rejects a merge when multiple source rows
match the same target row.

## Type 3 versus Type 2

| Requirement | Type 2 | Type 3 |
|---|---|---|
| Rows per business key | One row per version | One row |
| History retained | Complete history | Current and immediately previous value |
| Storage growth | Grows with every change | Bounded by the number of keys |
| Best for | As-of reporting and auditability | Before-versus-after comparisons |
| Main trade-off | More rows and temporal joins | Older history is overwritten |

## Try it

There is not yet a Type 3 notebook in the repository. To try the pattern in
Databricks, create the dimension table, load an initial ingress snapshot, then
change a customer's address and run the new, updated, deleted, and merge cells
again. The old address should appear in `c_address_previous` while the new
address appears in `c_address_current`.
