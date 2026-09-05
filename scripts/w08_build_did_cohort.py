"""One warehouse scan, cached. Builds the before/after cohort for the DiD analysis.

Design
------
Treated : pages whose last_optimized_date falls in May 2026.
Control : pages from the SAME clients that were never optimized, given the same
          calendar windows so any month-level trend hits both groups equally.
Windows : 30 days before the optimization date, 30 days after (day 0 excluded --
          the change lands sometime that day and we cannot tell when).

The fact table ends 2026-06-30, which is why May is the only month where every
treated page has a full 30 days on both sides.

Per the data rules: iterate on a sample, run the full scan ONCE, cache the result.
"""
import duckdb, time
from pathlib import Path
from huggingface_hub import get_token

OUT = Path("work/outputs"); OUT.mkdir(parents=True, exist_ok=True)
CACHE = OUT / "w08_did_cohort.parquet"

BASE = "hf://datasets/FlyRank/internship-warehouse"
DIM = f"{BASE}/dim_content.parquet"
FACT = [f"{BASE}/fact_content_daily_performance/month=2026-{m}/data_0.parquet"
        for m in ("04", "05", "06")]

con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs;")
con.execute(f"CREATE SECRET hf_tok (TYPE huggingface, TOKEN '{get_token()}');")

fact_union = " UNION ALL ".join(
    f"SELECT report_date, client_hash_id, content_hash_id, gsc_clicks, gsc_impressions, "
    f"gsc_data_available FROM '{f}'" for f in FACT)

SQL = f"""
WITH dim AS (
    SELECT client_hash_id, content_hash_id, last_optimized_date, word_count,
           search_volume, competition, content_type
    FROM '{DIM}'
    WHERE is_published AND NOT is_deleted
),
-- one anchor date per client: the day most of its pages were optimized in May
anchor AS (
    SELECT client_hash_id, last_optimized_date AS t0, COUNT(*) AS n,
           ROW_NUMBER() OVER (PARTITION BY client_hash_id ORDER BY COUNT(*) DESC) AS rk
    FROM dim
    WHERE last_optimized_date BETWEEN DATE '2026-05-01' AND DATE '2026-05-31'
    GROUP BY 1, 2
),
client_t0 AS (SELECT client_hash_id, t0 FROM anchor WHERE rk = 1),
-- treated uses its OWN optimization date; control borrows the client anchor
cohort AS (
    SELECT d.client_hash_id, d.content_hash_id, d.word_count, d.search_volume,
           d.competition, d.content_type,
           CASE WHEN d.last_optimized_date BETWEEN DATE '2026-05-01' AND DATE '2026-05-31'
                THEN 1 ELSE 0 END AS treated,
           CASE WHEN d.last_optimized_date BETWEEN DATE '2026-05-01' AND DATE '2026-05-31'
                THEN d.last_optimized_date ELSE c.t0 END AS t0
    FROM dim d
    JOIN client_t0 c USING (client_hash_id)
    WHERE d.last_optimized_date IS NULL
       OR (d.last_optimized_date BETWEEN DATE '2026-05-01' AND DATE '2026-05-31')
),
perf AS ({fact_union})
SELECT
    k.client_hash_id, k.content_hash_id, k.treated, k.t0,
    k.word_count, k.search_volume, k.competition, k.content_type,
    SUM(CASE WHEN p.report_date BETWEEN k.t0 - 30 AND k.t0 - 1 THEN p.gsc_clicks END)      AS clicks_pre,
    SUM(CASE WHEN p.report_date BETWEEN k.t0 + 1  AND k.t0 + 30 THEN p.gsc_clicks END)     AS clicks_post,
    SUM(CASE WHEN p.report_date BETWEEN k.t0 - 30 AND k.t0 - 1 THEN p.gsc_impressions END) AS impr_pre,
    SUM(CASE WHEN p.report_date BETWEEN k.t0 + 1  AND k.t0 + 30 THEN p.gsc_impressions END) AS impr_post,
    COUNT(DISTINCT CASE WHEN p.report_date BETWEEN k.t0 - 30 AND k.t0 - 1
                        THEN p.report_date END) AS days_pre,
    COUNT(DISTINCT CASE WHEN p.report_date BETWEEN k.t0 + 1 AND k.t0 + 30
                        THEN p.report_date END) AS days_post
FROM cohort k
JOIN perf p
  ON p.content_hash_id = k.content_hash_id
 AND p.client_hash_id  = k.client_hash_id
 AND p.gsc_data_available
 AND p.report_date BETWEEN k.t0 - 30 AND k.t0 + 30
GROUP BY 1,2,3,4,5,6,7,8
"""

if CACHE.exists():
    print(f"cache already present: {CACHE}")
else:
    t = time.time()
    print("scanning 3 monthly partitions (~35M rows)... this runs once")
    con.execute(f"COPY ({SQL}) TO '{CACHE.as_posix()}' (FORMAT PARQUET)")
    print(f"cached -> {CACHE}  ({CACHE.stat().st_size:,} bytes) in {time.time()-t:.0f}s")

df = con.execute(f"SELECT * FROM '{CACHE.as_posix()}'").df()
print(f"\nrows: {len(df):,}")
print(df.groupby("treated").size().rename("pages").to_string())
print(f"clients: {df.client_hash_id.nunique()}")
