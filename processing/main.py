import re
import time
import json
import random
import functools
from tqdm import tqdm
from pathlib import Path
from unidecode import unidecode
from argparse import ArgumentParser
import function as func

# python3 main.py --dataset "piston.my" --url_dataset "https://huggingface.co/datasets/mesolitica/crawl-my-website/resolve/main/piston.my.jsonl" --master_folder "/home/ubuntu/za/datasets02"


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--dataset", dest="dataset", help="Dataset name", required=True)
    parser.add_argument(
        "--url_dataset", dest="url_dataset", help="Dataset URL (jsonl)", required=True
    )
    parser.add_argument(
        "--master_folder",
        dest="master_dataset_folder",
        help="Master folder to store dataset and processed output",
        required=True,
    )
    parser.add_argument(
        "--mp_core",
        dest="mp_core",
        default=6,
        help="Postprocessing Core",
        required=False,
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    start_time = time.time()

    args = parse_arguments()

    dataset_name = args.dataset
    url_dataset = args.url_dataset
    master_dataset_folder = args.master_dataset_folder
    mp_core = args.mp_core

    func.init_process(url_dataset, master_dataset_folder, dataset_name)
    func.second_process(master_dataset_folder, dataset_name)
    func.third_process(master_dataset_folder, mp_core)
    before_dedup_mb, after_dedup_mb, after_post_mb = func.get_size(
        master_dataset_folder, dataset_name
    )

    print("\n\n====================")
    print(f"File Size - {dataset_name}")
    print(f"before_dedup    ---> {before_dedup_mb}")
    print(f"after_dedup     ---> {after_dedup_mb}")
    print(f"after_post      ---> {after_post_mb}")
    print("====================\n\n")

    print(f"--- {time.time() - start_time} seconds ---")
