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
        "--clean_file_path",
        dest="clean_file_path",
        help="Load the .jsonl file that has been cleaned instead of from huggingface",
        required=False,
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
    parser.add_argument(
        "--text_key",
        dest="text_key",
        nargs="+",
        help="Dict key contain text data",
        required=False,
    )

    args = parser.parse_args()
    return args


def loop_process(datasets, process_type="multi"):
    if process_type == "multi":
        lst_dataset, _ = datasets
    else:
        lst_dataset = datasets

    dataset_name_lst = []
    remove_dataset_name_lst = []

    for dataset in lst_dataset:
        try:
            url_dataset = dataset[1]
            dataset_name = dataset[0]

            dataset_name_lst.append(dataset_name)

            print(f"\nProcessing ... {dataset_name}\n")

            try:
                func.init_process(
                    raw_dataset_path=master_dataset_folder,
                    dataset_name=dataset_name,
                    clean_file_path=url_dataset,
                    text_key=text_key,
                )
            except:
                func.init_process(
                    raw_dataset_path=master_dataset_folder,
                    dataset_name=dataset_name,
                    link=url_dataset,
                    text_key=text_key,
                )

            func.second_process(master_dataset_folder, dataset_name)
        except Exception as e:
            print(f"[ERROR] {str(e)} \n Skip {dataset_name} ...")
            dataset_name_lst.remove(dataset_name)
            remove_dataset_name_lst.append(dataset_name)
            pass

    if len(dataset_name_lst) != 0:
        func.third_process(master_dataset_folder, mp_core)

        for l in dataset_name_lst:
            before_dedup_mb, after_dedup_mb, after_post_mb = func.get_size(
                master_dataset_folder, l
            )

            print("\n\n====================")
            print(f"File Size - {l}")
            print(f"before_dedup    ---> {before_dedup_mb}")
            print(f"after_dedup     ---> {after_dedup_mb}")
            print(f"after_post      ---> {after_post_mb}")
            print("====================\n\n")

    if len(remove_dataset_name_lst) > 0:
        print(f"Problem datasets:\n{','.join(remove_dataset_name_lst)}")


if __name__ == "__main__":
    start_time = time.time()

    global master_dataset_folder
    global mp_core
    global text_key

    args = parse_arguments()

    clean_file_path = args.clean_file_path
    multiple_dataset = args.dataset_with_link
    text_key = args.text_key

    if clean_file_path:
        print("[Run for manually cleaned dataset]")
        dataset_name = args.dataset
        datasets = [(dataset_name, clean_file_path)]
    elif multiple_dataset:
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
