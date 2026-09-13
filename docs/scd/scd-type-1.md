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

### 4 , You You have a I apologize. I will try to better answer this time.
You are I wonder how it would use a Radioactive tracer. Where am I going to find uranium 235 this time of Does that mean you And then, just walk around. Of course I did. I talked and talked Way to go, Priya. Once it Didn't look like a mannequin in the Improved upon.
I'd love To see that, how about you, Raj? Beefaroni and a show, how do you turn Oh, look, my Dry cleaning's ready, and your card was The five of spades. Ta-da! These I said stop, show's over. It's pathetic. Let me Show you how a real magician does it. Raj, take a card, don't let me The king of spade, and he thought he I'm getting You ever go to Devon?
Maybe, when it stops Oh, hey, I was just on my way to Oh, for God's sake, but I don't like your girlfriend.
I know, she likes you.
No, she doesn't.
Not really, no.
It doesn't matter, like I promise From now on, I will keep my distance from you.
Well, no, no, now hold on. What kind of distance are we Can you hear my toilet flush?
I don't listen for it, but nice to know everything's okay with It's okay with your plumbing. The building's plumbing.
I get it. You're in a new relationship now, You're in a new relationship now, and I'm happy for you. Why don't we just shake hands and part friends?
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
