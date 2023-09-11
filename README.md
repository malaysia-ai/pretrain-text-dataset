# text-dataset-dedup

Dedup and postprocessing for text dataset gathered from https://github.com/users/huseinzol05/projects/1

All dedup and postprocessed dataset uploaded at https://huggingface.co/datasets/malaysia-ai/dedup-text-dataset

Checkout deduping process at https://docs.google.com/spreadsheets/d/1IKnFlx3Ax-IDBwedUdZo0-v8oyFErvcc7MfI1bu55vQ/edit?usp=sharing

## Server spec

1. 24 cores.
2. 220 GB RAM.

**Deduping can explode the memory, easily eat up to 30 GB if the dataset is > 10GB, so beware**.

## Download dataset

1. Most of download files are straight forward,

```bash
wget https://huggingface.co/datasets/mesolitica/crawl-amanz-my/resolve/main/parsed.jsonl -O hf-datasets/raw-datasets/amanz.jsonl
```

But sometime we have to some preprocessing like,

- [process-lowyat.ipynb](process-lowyat.ipynb)
- [process-data.gov.my.ipynb](process-data.gov.my.ipynb)
- [process-snapshot.ipynb](process-snapshot.ipynb)

We save raw datasets at [hf-datasets/raw-datasets](hf-datasets/raw-datasets).

## Text dedup

1. Clone [remove-duplicate-text-dataset.ipynb](remove-duplicate-text-dataset.ipynb) to new notebook, eg, [remove-duplicate-text-dataset-lowyat.ipynb](remove-duplicate-text-dataset-lowyat.ipynb).

This notebook use [text_dedup](text_dedup) to do dedup, borrowed from https://github.com/ChenghaoMou/text-dedup

All dedup datasets will save at [hf-datasets/dedupe-datasets](hf-datasets/dedupe-datasets).

## Postprocessing

1. Run [postprocessing.ipynb](postprocessing.ipynb) to start postprocessing,

- remove texts that contain HTTP errors.
- remove texts less than 3 characters.
- replace 6 spaces or more with 6 spaces.
- replace 6 dots or more with 6 dots.

**Rerun this notebook will not overwrite postprocessed datasets**.

## Calculate tokens using Llama2 tokenizer

1. Run [calculate-token-size.ipynb](calculate-token-size.ipynb) to calculate total tokens.

**Rerun this notebook will not recalculate the same datasets**.

## Merge and prepare to huggingface dataset

**There is no consideration AI alignment and safety in current dataset, we only apply basic postfilter**.

1. Run [combine.ipynb](combine-v2.ipynb),

This will combine most datasets into 1 JSONL file.

- 31.4 GB.

2. Run [prepare-tokenizer.ipynb](prepare-tokenizer.ipynb),

This will tokenized and cached the dataset.

3. Run [prepare-dataset-32768.ipynb](prepare-dataset-32768.ipynb),

This will partitioned tokenized dataset into 32768 context length.

## end-to-end processing using Python script

Released as a Python library, https://github.com/malaysia-ai/clean_text_my

