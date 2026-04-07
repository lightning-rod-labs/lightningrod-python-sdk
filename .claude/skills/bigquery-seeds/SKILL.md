---
name: bigquery-seeds
description: BigQuery seed sourcing patterns for Lightningrod. Use when sourcing seeds from BigQuery tables.
---

# BigQuery Seeds

## BigQuerySeedGenerator

```python
from lightningrod import BigQuerySeedGenerator

seed_generator = BigQuerySeedGenerator(
    query="SELECT text, created_at FROM `bigquery-public-data.hacker_news.full` LIMIT 1000",
    seed_text_column="text",
    date_column="created_at",
    max_rows=100,  # Start small for iteration
)
```

**No GCP account or credentials required.** Lightningrod manages BigQuery access and billing internally. The user does not need to set up a Google Cloud project or provide any credentials. **Never ask the user if they have a GCP project, BigQuery access, or Google Cloud credentials — they don't need any.**

**Supported datasets: any publicly queryable BigQuery dataset.** Because Lightningrod uses its own GCP project credentials under the hood, any dataset that is open to any GCP project without requiring explicit IAM access grants will work. This includes `bigquery-public-data.*` but also community-hosted public datasets like `githubarchive.*`. Private or user-owned BigQuery tables (those requiring a specific account to be granted access) are not supported.

**Commercial datasets like Crunchbase or PitchBook are NOT available** through BigQuery — do not recommend them as BigQuery sources. If the best data for a use case is behind a paywall (e.g. startup funding data), acknowledge this honestly and propose alternatives using what IS available in public BigQuery datasets, or suggest the user provide their own data.

**If unsure whether a dataset is queryable**, try a schema inspection query first — if it returns results without an access error, it works.

## Known queryable datasets

The full registry of BigQuery public datasets is browsable at [Google Cloud Marketplace — Datasets](https://console.cloud.google.com/marketplace/browse?filter=solution-type:dataset). Below are notable datasets that work well as Lightningrod seed sources:

| Dataset | Description | Useful tables |
|---------|-------------|---------------|
| `bigquery-public-data.hacker_news` | HN posts and comments | `full`, `stories` |
| `bigquery-public-data.github_repos` | GitHub commit metadata and file contents | `commits`, `contents`, `languages` |
| `bigquery-public-data.stackoverflow` | SO questions and answers | `posts_questions`, `posts_answers`, `tags` |
| `bigquery-public-data.wikipedia` | Wikipedia article text | `pageviews_*`, `articles` |
| `bigquery-public-data.google_trends` | Google Trends search interest data | `top_terms`, `top_rising_terms` |
| `bigquery-public-data.usa_names` | US baby name popularity by year | `usa_1910_current` |
| `bigquery-public-data.noaa_gsod` | Global weather station observations | `gsod*` |
| `bigquery-public-data.austin_bikeshare` | Austin bike share trip data | `bikeshare_trips`, `bikeshare_stations` |
| `bigquery-public-data.san_francisco_311` | SF 311 service requests | `311_service_requests` |
| `bigquery-public-data.new_york_taxi_trips` | NYC taxi trip records | `tlc_yellow_trips_*` |
| `bigquery-public-data.sec_quarterly_financials` | SEC financial statements | `financials` |
| `bigquery-public-data.gdelt_samples` | GDELT news events | `full` |
| `bigquery-public-data.crypto_bitcoin` | Bitcoin blockchain data | `transactions`, `blocks` |
| `githubarchive.*` | GitHub event stream by year/month/day (stars, forks, PRs, issues) — see [gharchive.org](https://www.gharchive.org/#bigquery) | `githubarchive.year.*`, `githubarchive.month.*`, `githubarchive.day.*` |

Other public datasets likely work too — browse the registry or verify with a schema inspection query before committing to them.

**Important: Crunchbase, PitchBook, and other commercial datasets are NOT available.** Only datasets that are publicly queryable without special access grants work through Lightningrod. Do not recommend datasets that require paid subscriptions or private access.

## Schema inspection

Before writing the seed query, inspect the table schema:

```sql
SELECT column_name, data_type
FROM `bigquery-public-data.hacker_news.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'full'
ORDER BY ordinal_position
```

Or preview rows:

```sql
SELECT * FROM `bigquery-public-data.hacker_news.full` LIMIT 5
```

## Label-in-SQL pattern

When ground truth is available in the table (e.g. upvote scores, accepted answers), embed it in the seed text so `QuestionAndLabelGenerator` can extract it — no separate labeler needed:

```sql
SELECT
  CONCAT(
    'Title: ', title, '\n',
    'Score: ', CAST(score AS STRING), '\n',
    'Text: ', COALESCE(text, '')
  ) AS seed_text,
  timestamp AS date
FROM `bigquery-public-data.hacker_news.stories`
WHERE score IS NOT NULL
LIMIT 500
```

Then pair with `QuestionAndLabelGenerator`, which extracts both the question and label from the seed text.

## Reference

See `notebooks/getting_started/03_bigquery_datasource.ipynb` for a full example.
