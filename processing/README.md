# text-dataset-dedup-py

## Description
The `text-dataset-dedup-py` repository contains a Python script that performs a deduplication process on a text dataset. This process is implemented based on the code provided in the [Jupyter Notebook](https://github.com/malaysia-ai/text-dataset-dedup).

## How to Use
Follow the steps below to use the deduplication script:

1. **Change Directory**: Navigate to the `/processing` directory within this repository.

2. **Prepare the Command**: Once in the `/processing` directory, prepare the command to execute the deduplication process. 

```bash
python3 main.py --dataset "piston.my" --url_dataset "https://huggingface.co/datasets/mesolitica/crawl-my-website/resolve/main/piston.my.jsonl" --master_folder "/home/ubuntu/za/datasets04"
```
### Arguments
1. `dataset`: Name of the dataset folder inside /dataset where the script will find data. *REQUIRED
2. `url_dataset`: URL of the JSONL file containing data to be processed (script only handles JSONL files). *REQUIRED
3. `master_folder`: Absolute path to the master directory where the deduplication process will occur. *REQUIRED



