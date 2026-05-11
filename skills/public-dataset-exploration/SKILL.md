---
name: public-dataset-exploration
description: Explore Kaggle, Hugging Face, GitHub for raw datasets to convert to seeds. Use when user has a domain but no data.
---

# Public Dataset Exploration

## When to use

User has a domain (e.g. "sports forecasting", "medical Q&A") but no documents. Explore public marketplaces for raw datasets that can become seeds.

## Marketplaces

- **Kaggle:** kaggle.com/datasets — search by topic, check license
- **Hugging Face:** huggingface.co/datasets — many formats, often with load_dataset()
- **GitHub:** awesome-datasets, domain-specific repos — raw CSVs, JSON, text

## Criteria for "relevant but not training-ready"

Look for:
- Raw or semi-structured data (articles, reports, event logs, tables)
- Not already Q&A pairs or instruction-following format
- Content that could yield forecasting questions or document-based Q&A
- Reasonable license for use

Avoid:
- Already fine-tuned / instruction datasets
- Purely synthetic or already labeled for training

## Flow

1. Search marketplaces for domain + "dataset" or "raw data"
2. Identify 1–3 candidates; check format (CSV, JSON, PDF, text)
3. Download (Kaggle API, huggingface_hub, git clone, or wget)
4. Convert to samples via files_to_samples or file_to_samples
5. Create input dataset with lr.datasets.create_from_samples
6. Add notebook cells for download + conversion + pipeline

## Minimal iteration

Download a small subset first (e.g. first 10 files, or head of CSV). Validate pipeline before full download.
