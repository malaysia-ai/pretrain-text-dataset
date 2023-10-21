# text-dataset-dedup

Dedup and postprocessing for text dataset gathered from https://github.com/users/huseinzol05/projects/1

All dedup and postprocessed dataset uploaded at https://huggingface.co/datasets/malaysia-ai/dedup-text-dataset

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

## Prepare for training session

**There is no consideration AI alignment and safety in current dataset, we only apply basic postfilter**.

### Llama2

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

### Mistral

This step to prepare FPF Mistral model.

1. Run [mistral/combine-mistral.ipynb](mistral/combine-mistral.ipynb),

This will combine most datasets into 1 JSONL file.

- 32.6 GB.

2. Run [mistral/prepare-tokenizer.ipynb](mistral/prepare-tokenizer.ipynb),

This will tokenized and cached the dataset.

3. Run [mistral/prepare-dataset-4096.ipynb](mistral/prepare-dataset-4096.ipynb),

This will partitioned tokenized dataset into 4096 context length.

### Pretrain

This step to prepare pretrain models from scratch.

1. Run [pretrain/combine-lm.ipynb](pretrain/combine-lm.ipynb),

This will combine all datasets into 1 JSONL file.

- 81 GB.
- 16994238464 tokens.

2. Run [pretrain/tokenizer-4096.ipynb](pretrain/tokenizer-4096.ipynb),

This will tokenized and partitioned tokenized dataset into 4096 context length.

3. Run [pretrain/from-pyarrow-to-mosaic.ipynb](pretrain/from-pyarrow-to-mosaic.ipynb),

This will convert PyArrow streaming format into MosaicML streaming format.

4. Run [pretrain/combine-mosaicml.ipynb](pretrain/combine-mosaicml.ipynb),

This will combine multiple MosaicML streaming folders into 1 folder.

## end-to-end processing using Python script

Released as a Python library, https://github.com/malaysia-ai/clean_text_my

