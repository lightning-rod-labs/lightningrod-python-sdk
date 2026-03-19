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

**No GCP account or credentials required.** Lightningrod manages BigQuery access and billing internally. The user does not need to set up a Google Cloud project or provide any credentials.

**Supported datasets: any publicly queryable BigQuery dataset.** Because Lightningrod uses its own GCP project credentials under the hood, any dataset that is open to any GCP project without requiring explicit IAM access grants will work. This includes `bigquery-public-data.*` but also community-hosted public datasets like `githubarchive.*`. Private or user-owned BigQuery tables (those requiring a specific account to be granted access) are not supported.

**If unsure whether a dataset is queryable**, try a schema inspection query first — if it returns results without an access error, it works.

## Known queryable datasets

| Dataset | Description | Useful tables |
|---------|-------------|---------------|
| `bigquery-public-data.hacker_news` | HN posts and comments | `full`, `stories` |
| `bigquery-public-data.github_repos` | GitHub commit metadata and file contents | `commits`, `contents` |
| `bigquery-public-data.gdelt_samples` | GDELT news events | `full` |
| `bigquery-public-data.stackoverflow` | SO questions and answers | `posts_questions`, `posts_answers` |
| `bigquery-public-data.wikipedia` | Wikipedia article text | `articles` |
| `githubarchive.*` | GitHub event stream by year/month/day (stars, forks, PRs, issues) — see [gharchive.org](https://www.gharchive.org/#bigquery) | `githubarchive.year.*`, `githubarchive.month.*`, `githubarchive.day.*` |

Other community-hosted public datasets likely work too — verify with a schema inspection query before committing to them.

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
