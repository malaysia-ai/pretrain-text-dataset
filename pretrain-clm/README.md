# Pretrain CLM

This is to pretrain 100M - 500M parameters CLM. All steps done using Standard_F48s_v2 node size.

This step to prepare pretrain models from scratch.

## how-to

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