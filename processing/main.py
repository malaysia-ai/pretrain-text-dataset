import re
import mp
import time
import json
import random
import functools
from tqdm import tqdm
from pathlib import Path
from unidecode import unidecode
from argparse import ArgumentParser
import function as func


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        "--dataset", dest="dataset", help="Dataset name", required=False
    )
    parser.add_argument(
        "--url_dataset", dest="url_dataset", help="Dataset URL (jsonl)", required=False
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
    parser.add_argument(
        "--dataset_with_link",
        dest="dataset_with_link",
        nargs="+",
        help="Dataset name",
        required=False,
    )

    args = parser.parse_args()
    return args


def loop_process(datasets, process_type="multi"):
    if process_type == "multi":
        lst_dataset, _ = datasets
    else:
        lst_dataset = datasets

    for dataset in lst_dataset:
        url_dataset = dataset[1]
        dataset_name = dataset[0]

        print(f"\nProcessing ... {dataset_name}\n")

        func.init_process(url_dataset, master_dataset_folder, dataset_name)
        func.second_process(master_dataset_folder, dataset_name)
        func.third_process(master_dataset_folder, 6)
        before_dedup_mb, after_dedup_mb, after_post_mb = func.get_size(
            master_dataset_folder, dataset_name
        )

        print("\n\n====================")
        print(f"File Size - {dataset_name}")
        print(f"before_dedup    ---> {before_dedup_mb}")
        print(f"after_dedup     ---> {after_dedup_mb}")
        print(f"after_post      ---> {after_post_mb}")
        print("====================\n\n")


if __name__ == "__main__":
    start_time = time.time()

    global master_dataset_folder

    args = parse_arguments()

    multiple_dataset = args.dataset_with_link

    if multiple_dataset:
        print("[Run for MULTIPLE datasets]")
        datasets = [tuple(l.split(",")) for l in multiple_dataset]
    else:
        print("[Run for SINGLE dataset]")
        dataset_name = args.dataset
        url_dataset = args.url_dataset

        datasets = [(dataset_name, url_dataset)]

    master_dataset_folder = args.master_dataset_folder
    mp_core = args.mp_core

    if len(datasets) // mp_core == 0:
        loop_process(datasets, process_type="single")
    else:
        mp.multiprocessing(datasets, loop_process, cores=mp_core, returned=False)

    print(f"--- {time.time() - start_time} seconds ---")
