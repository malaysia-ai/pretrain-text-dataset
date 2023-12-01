# Prepare dataset for Mistral FPF

This step to prepare FPF Mistral model.

<<<<<<< HEAD
1. Run [combine-mistral.ipynb](combine-mistral.ipynb),
=======
## how-to

1. Run [mistral/combine-mistral.ipynb](mistral/combine-mistral.ipynb),
>>>>>>> 0ad2625bb3fbae74dc9b77763900b56f49929a7f

This will combine most datasets into 1 JSONL file.

- 32.6 GB.

2. Run [prepare-tokenizer.ipynb](prepare-tokenizer.ipynb),

This will tokenized and cached the dataset.

3. Run [prepare-dataset-4096.ipynb](prepare-dataset-4096.ipynb),

This will partitioned tokenized dataset into 4096 context length.