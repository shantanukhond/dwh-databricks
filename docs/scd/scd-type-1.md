---
title: Type 1 · Overwrite
---
Type 1 slowly changing dimensions (SCDs) overwrite the existing dimension
record when an attribute changes. When a customer changes address, the old
address is replaced by the new address in the same row.
This is useful when reporting only needs the latest value and historical values
are not required.

## Dimension shape
The dimension keeps one row per customer and stores the latest descriptive
attributes:

```sql
CREATE OR REPLACE TABLE sandbox.bronze.customer (
	id BIGINT GENERATED ALWAYS AS IDENTITY,
	c_custkey BIGINT,
	c_name STRING,
	c_address STRING,
	c_phone STRING,
	c_nationkey BIGINT,
	c_mktsegment STRING,
	last_updated_at TIMESTAMP
) USING DELTA;

There are no effective dates or previous-value columns. The latest source
value always wins.

## Process
We do these changes in multiple phases and steps as follows

### 1. Identify New Records
This is simple Left Anti Join. We find records which are available in ingress
table but not available in bronze table so that they can be loaded.

```python
new_df = ing_df.alias("ing").join(
		brz_df.alias("brz"),
		col("ing.c_custkey") == col("brz.c_custkey"),
		"leftanti"
	)

new_df = new_df.withColumn("last_updated_at", lit(datetime.now()))
display(new_df)

### 2. Identify Updated Records
Here we find records which are available in both ingress and bronze but have a
different value. Unlike Type 2, we update the existing row instead of closing
it and inserting another version.
```python
updated_df = ing_df.alias("ing").join(
		brz_df.alias("brz"),
		"inner"
	).filter(
		(col("ing.c_name") != col("brz.c_name")) |
		(col("ing.c_address") != col("brz.c_address")) |
		(col("ing.c_phone") != col("brz.c_phone")) |
		(col("ing.c_nationkey") != col("brz.c_nationkey")) |
		(col("ing.c_mktsegment") != col("brz.c_mktsegment"))
	).select("ing.*").withColumn(
		"last_updated_at", lit(datetime.now())
	)

display(updated_df)

### 3. Identify Deleted Records
This is similar to identifying new records but the opposite direction. It
finds records in bronze that are missing in ingress.

In a Type 1 dimension, deletion handling depends on the business requirement.
You can physically delete the record, or add an `is_active` column and mark it
inactive. For this demo, we leave deletion handling to the consuming process
and focus on the Type 1 overwrite behavior.
### 4. Merge the Changes
The new and updated records can be applied with one Delta Lake `MERGE`. New
records are inserted and existing records are overwritten with the latest
values.

```python
from delta.tables import DeltaTable

customer_dim = DeltaTable.forName(spark, "sandbox.bronze.customer")
customer_dim.alias("brz").merge(
	updated_df.unionByName(new_df, allowMissingColumns=True).alias("ing"),
	"brz.c_custkey = ing.c_custkey",
).whenMatchedUpdateAll(
).whenNotMatchedInsertAll(
).execute()

In production, build the change sets so that each business key appears only
once in the merge source. Delta Lake rejects a merge when multiple source rows
match the same target row.

## Type 1 versus Type 2

| Requirement | Type 1 | Type 2 |
|---|---|---|
| Rows per business key | One row | One row per version |
| History retained | No history | Complete history |
| Storage growth | Bounded by number of keys | Grows with every change |
| Best for | Current-state reporting | As-of reporting and auditability |

## Try it

Load the initial customer data, then change a customer's address in ingress
and run the comparison and merge cells again. The existing dimension row is
overwritten, and only the new address remains.
---
title: Type 1 · Overwrite
---

Type 1 slowly changing dimensions (SCDs) overwrite the existing dimension
record when an attribute changes. When a customer changes address, the old
address is replaced by the new address in the same row.

This is useful when reporting only needs the latest value and historical values
are not required.

## Dimension shape

The dimension keeps one row per customer and stores the latest descriptive
attributes:

```sql
CREATE OR REPLACE TABLE sandbox.bronze.customer (
	id BIGINT GENERATED ALWAYS AS IDENTITY,
	c_custkey BIGINT,
	c_name STRING,
	c_address STRING,
	c_phone STRING,
	c_nationkey BIGINT,
	c_mktsegment STRING,
	last_updated_at TIMESTAMP
) USING DELTA;
```

There are no effective dates or previous-value columns. The latest source
value always wins.

## Process
We do these changes in multiple phases and steps as follows

### 1. Identify New Records
This is simple Left Anti Join. We find records which are available in ingress
table but not available in bronze table so that they can be loaded.

```python
new_df = ing_df.alias("ing").join(
		brz_df.alias("brz"),
		col("ing.c_custkey") == col("brz.c_custkey"),
		"leftanti"
	)

new_df = new_df.withColumn("last_updated_at", lit(datetime.now()))

display(new_df)
```

### 2. Identify Updated Records
Here we find records which are available in both ingress and bronze but have a
different value. Unlike Type 2, we update the existing row instead of closing
it and inserting another version.

```python
updated_df = ing_df.alias("ing").join(
		brz_df.alias("brz"),
		col("ing.c_custkey") == col("brz.c_custkey"),
		"inner"
	).filter(
		(col("ing.c_name") != col("brz.c_name")) |
		(col("ing.c_address") != col("brz.c_address")) |
		(col("ing.c_phone") != col("brz.c_phone")) |
		(col("ing.c_nationkey") != col("brz.c_nationkey")) |
		(col("ing.c_mktsegment") != col("brz.c_mktsegment"))
	).select("ing.*").withColumn(
		"last_updated_at", lit(datetime.now())
	)

display(updated_df)
```

### 3. Identify Deleted Records
This is similar to identifying new records but the opposite direction. It
finds records in bronze that are missing in ingress.

In a Type 1 dimension, deletion handling depends on the business requirement.
You can physically delete the record, or add an `is_active` column and mark it
inactive. For this demo, we leave deletion handling to the consuming process
and focus on the Type 1 overwrite behavior.

### 4. Merge the Changes
```python
Well, now hold on, let me... How Hold on, how about this? How about We still hang out, but on the Damn Why so gum-chunk? Apparently, you can't hack into a You have to get into a government supercomputer and then Try to buy uranium without the Department of Homeland Security tattling to Oh, that's God. God! Dude! I'm not going to talk with you. Such a mean person I'm He had to go to the house. I I don't know, I Oh, this time he did feeling bad. It's Oh, what? I thought It's not No, I I just What? To shout, I To I was By the I think I should explain this. Coffee. Coffee. Coffee. Coffee. Coffee. Coffee... What does MMT calling you should do? Three spoon of sugar and Do you know Save electricity, save It's not good. I should stop then For Oh, they asked me that.erwritten with the latest
values.

```python
from delta.tables import DeltaTable

customer_dim = DeltaTable.forName(spark, "sandbox.bronze.customer")

customer_dim.alias("brz").merge(
	updated_df.unionByName(new_df, allowMissingColumns=True).alias("ing"),
	"brz.c_custkey = ing.c_custkey",
).whenMatchedUpdateAll(
).whenNotMatchedInsertAll(
).execute()
```

In production, build the change sets so that each business key appears only
once in the merge source. Delta Lake rejects a merge when multiple source rows
match the same target row.

## Type 1 versus Type 2

| Requirement | Type 1 | Type 2 |
|---|---|---|
| Rows per business key | One row | One row per version |
| History retained | No history | Complete history |
| Storage growth | Bounded by number of keys | Grows with every change |
| Best for | Current-state reporting | As-of reporting and auditability |

## Try it

Load the initial customer data, then change a customer's address in ingress
and run the comparison and merge cells again. The existing dimension row is
overwritten, and only the new address remains.
