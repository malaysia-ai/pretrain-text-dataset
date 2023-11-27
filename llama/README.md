# Prepare dataset for Llama2 FPF

This step to prepare FPF Llama2 models.

1. Run [llama/combine-v2.ipynb](llama/combine-v2.ipynb),

This will combine most datasets into 1 JSONL file.

- 31.4 GB.

2. Run [llama/prepare-tokenizer.ipynb](llama/prepare-tokenizer.ipynb),

This will tokenized and cached the dataset.

3. Run [llama/prepare-dataset-2048.ipynb](llama/prepare-dataset-2048.ipynb),

This will partitioned tokenized dataset into 2048 context length.

4. Run [llama/prepare-dataset-32768.ipynb](llama/prepare-dataset-32768.ipynb),

This will partitioned tokenized dataset into 32768 context length.