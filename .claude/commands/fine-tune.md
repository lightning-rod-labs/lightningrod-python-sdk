Start a fine-tuning workflow. The orchestrator will coordinate dataset generation (if needed) and fine-tuning, iterating toward good training results.

Use this when you:
- Already have a Lightningrod dataset and want to fine-tune a model on it
- Want to generate a dataset and immediately fine-tune
- Want to evaluate an existing fine-tuned model

Describe your goal — for example:
- "Fine-tune on my existing dataset ds_abc123"
- "Generate a forecasting dataset from news and fine-tune a model end-to-end"
- "Evaluate model model_xyz against gpt-4o on my test set"

The orchestrator will estimate costs before running any training jobs.
