# text-dataset-dedup-py

## Description
The `text-dataset-dedup-py` repository contains a Python script that performs a deduplication process on a text dataset. This process is implemented based on the code provided in the [Jupyter Notebook](https://github.com/malaysia-ai/text-dataset-dedup).

## How to Use
Follow the steps below to use the deduplication script:

1. **Change Directory**: Navigate to the `/processing` directory within this repository.

2. **Prepare the Command**: Once in the `/processing` directory, prepare the command to execute the deduplication process. 

Single Dataset (from Huggingface URL)
```bash
python3 main.py --dataset "piston.my" --url_dataset "https://huggingface.co/datasets/mesolitica/crawl-my-website/resolve/main/piston.my.jsonl" --master_folder "/home/ubuntu/za/datasets04" --text_key reviews_html reviews_text
```

Single Dataset (manually cleaned)
```bash
python3 main.py --dataset "murai.my" --clean_file_path "/home/ubuntu/faiq913_folder/Cleaned Huggingface datasets/murai.my/murai_my_clean.jsonl" --master_folder "/home/ubuntu/za/datasets04"
```

If you have multiple datasets from multiple Huggingface URLs,
```bash
python3 main.py \
--master_folder "/home/ubuntu/za/datasets04" \
--dataset_with_link \
piston.my,https://huggingface.co/datasets/mesolitica/crawl-my-website/resolve/main/piston.my.json \
piston2,https://huggingface.co/datasets/mesolitica/crawl-my-website/resolve/main/piston.my.jsonl \
piston3,https://huggingface.co/datasets/mesolitica/crawl-my-website/resolve/main/piston.my.jsonl
```

### Arguments
1. `dataset`: Name of the dataset folder inside /dataset where the script will find data.
2. `url_dataset`: URL of the JSONL file containing data to be processed (script only handles JSONL files). 
3. `master_folder`: Absolute path to the master directory where the deduplication process will occur.
4. `dataset_with_link`: Format {dataset_name},{dataset_url} {dataset_name02},{dataset_url02}
5. `text_key`: To add own custom key if you encounter an issue `dataset not in standard key-value. must have ...`



