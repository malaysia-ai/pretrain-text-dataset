import os
import mp
import json
import functools
import subprocess
import utils as ut
from glob import glob
from tqdm import tqdm
from pathlib import Path
from datasets import Dataset
from unidecode import unidecode


def download_dataset(link, raw_dataset_path, dataset_name):
    try:
        global MAIN_FOLDER_DATASET

        MAIN_FOLDER_DATASET = f"{raw_dataset_path}/raw-datasets/"
        ut.create_dir(MAIN_FOLDER_DATASET)

        command = f"wget {link} -O {MAIN_FOLDER_DATASET}/{dataset_name}.jsonl"
        ut.run_command(command)

        return True
    except:
        return False


def init_process(
    raw_dataset_path, dataset_name, text_key=None, link=None, clean_file_path=None
):
    global INITIAL_PRE_PROCESSING_FOLDER
    global MAIN_FOLDER_DATASET

    txt_l = []

    if link != None:
        dd = download_dataset(link, raw_dataset_path, dataset_name)

        INITIAL_PRE_PROCESSING_FOLDER = f"{raw_dataset_path}/staging-datasets/"
        ut.create_dir(INITIAL_PRE_PROCESSING_FOLDER)

        with open(f"{MAIN_FOLDER_DATASET}/{dataset_name}.jsonl") as fopen:
            data = [json.loads(line) for line in fopen]

    if clean_file_path != None:
        MAIN_FOLDER_DATASET = clean_file_path

        INITIAL_PRE_PROCESSING_FOLDER = f"{raw_dataset_path}/staging-datasets/"
        ut.create_dir(INITIAL_PRE_PROCESSING_FOLDER)

        with open(clean_file_path) as fopen:
            data = [json.loads(line) for line in fopen]

    try:
        key_data = [key for key, _ in data[0].items()]
        print(f"Availble key -> {key_data}")
    except AttributeError:
        raise Exception(
            f"dataset not in standard list format, total record in the file -> {len(data)}."
        )

    suitable_key = [
        "p",
        "text",
        "article_text",
        "article_body",
        "text",
        "content",
        "contents",
        "body",
        "articleBody",
        "data",
        "title",
    ]

    if text_key:
        suitable_key = list(set(suitable_key + text_key))

    if not any(key in key_data for key in suitable_key):
        raise Exception(
            f"dataset not in standard key-value. must have ({' | '.join(suitable_key)})"
        )

    for i in tqdm(data):
        str_lst = []
        for key in i.keys():
            if key in suitable_key:
                str_lst.append(str(i[key]))
            else:
                continue

        if None in str_lst:
            str_lst = ["None" if v is None else v for v in str_lst]

        str_data = "\n\n".join(str_lst)
        txt_l.append({"text": f"{str_data}"})

    ut.write_to_json(txt_l, f"{INITIAL_PRE_PROCESSING_FOLDER}{dataset_name}.jsonl")


def second_process(raw_dataset_path, dataset_name):
    global HF_FOLDER_RAW
    global HF_FOLDER_DEDUPE

    HF_FOLDER_RAW = f"{raw_dataset_path}/hf-datasets/raw-datasets/"
    HF_FOLDER_DEDUPE = f"{raw_dataset_path}/hf-datasets/dedupe-datasets/"

    ut.create_dir(HF_FOLDER_RAW)
    ut.create_dir(HF_FOLDER_DEDUPE)

    with open(f"{INITIAL_PRE_PROCESSING_FOLDER}/{dataset_name}.jsonl") as fopen:
        data = [json.loads(line) for line in fopen]

    print(f"total records: {len(data)}")

    data = [entry for entry in tqdm(data) if entry is not None]

    print(f"total records after remove None: {len(data)}")

    data_dict = {"text": [entry["text"] for entry in data]}

    dataset = Dataset.from_dict(data_dict)

    dataset.save_to_disk(f"{HF_FOLDER_RAW}{dataset_name}")

    command = f"python3 -m text_dedup.minhash \
                --path {HF_FOLDER_RAW}{dataset_name} \
                --split train \
                --cache_dir ./cache \
                --output {HF_FOLDER_DEDUPE}{dataset_name} \
                --column text \
                --batch_size 10000 \
                --threshold 0.95 \
                --min_length 1 \
                --local"

    ut.run_command(command)


def third_process(raw_dataset_path, mp_core):
    HF_FOLDER_POSTPROCESSING = f"{raw_dataset_path}/hf-datasets/postprocessing/"
    HF_FOLDER_POSTPROCESSING_DONE = (
        f"{raw_dataset_path}/hf-datasets/postprocessing-done/"
    )

    ut.create_dir(HF_FOLDER_POSTPROCESSING)
    ut.create_dir(HF_FOLDER_POSTPROCESSING_DONE)

    files_lst = glob(f"{HF_FOLDER_DEDUPE}*.jsonl")

    print(f"total files to postprocessing --> {len(files_lst)}")

    core = mp_core

    if len(files_lst) // core == 0:
        process_type = "single"
        ut.loop(files_lst, process_type=process_type)
    else:
        process_type = "multi"
        mp.multiprocessing(files_lst, ut.loop, cores=core, returned=False)


def get_size(raw_dataset_path, dataset_name):
    before_dedup_url = f"{MAIN_FOLDER_DATASET}/{dataset_name}.jsonl"
    before_dedup_clean = f"{MAIN_FOLDER_DATASET}"
    after_dedup = f"{HF_FOLDER_DEDUPE}{dataset_name}.jsonl"
    after_post = f"{raw_dataset_path}/hf-datasets/postprocessing/{dataset_name}.jsonl"

    try:
        before_dedup_mb = (os.stat(before_dedup_url)).st_size / (1024 * 1024)
    except:
        before_dedup_mb = (os.stat(before_dedup_clean)).st_size / (1024 * 1024)

    after_dedup_mb = (os.stat(after_dedup)).st_size / (1024 * 1024)
    after_post_mb = (os.stat(after_post)).st_size / (1024 * 1024)

    return (
        f"{before_dedup_mb:.2f} MB",
        f"{after_dedup_mb:.2f} MB",
        f"{after_post_mb:.2f} MB",
    )
