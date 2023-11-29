# Prepare dataset for Yi FPF

This step to prepare FPF Yi models.

## how-to

1. Run [combine-dataset.ipynb](combine-dataset.ipynb),

This will combine most datasets into 1 JSONL file.

- 41 GB.

2. Run [convert-mosaic.ipynb](prepare-tokenizer.ipynb),

This will tokenized and convert into mosaic format.

3. Run [combine-mosaic-all.ipynb](combine-mosaic-all.ipynb),

This will combine all mosaic partitions into one mosaic folder, total 14114934784 tokens.