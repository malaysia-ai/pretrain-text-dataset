import os
import re
import json
import subprocess
from tqdm import tqdm
from pathlib import Path


def is_dir(path):
    return os.path.isdir(path)


def run_command(txt):
    subprocess.run(txt, shell=True)


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def write_to_json(lst, fn):
    with open(fn, "w+") as file:
        for item in tqdm(lst):
            x = json.dumps(item, ensure_ascii=False)
            file.write(x + "\n")


http_errors = [
    "400 Bad Request",
    "401 Unauthorized",
    "402 Payment Required",
    "403 Forbidden",
    "404 Not Found",
    "405 Method Not Allowed",
    "406 Not Acceptable",
    "407 Proxy Authentication Required",
    "408 Request Timeout",
    "409 Conflict",
    "410 Gone",
    "411 Length Required",
    "412 Precondition Failed",
    "413 Payload Too Large",
    "414 URI Too Long",
    "415 Unsupported Media Type",
    "416 Range Not Satisfiable",
    "417 Expectation Failed",
    "418 I'm a teapot",
    "421 Misdirected Request",
    "422 Unprocessable Entity",
    "423 Locked",
    "424 Failed Dependency",
    "425 Too Early",
    "426 Upgrade Required",
    "428 Precondition Required",
    "429 Too Many Requests",
    "431 Request Header Fields Too Large",
    "451 Unavailable For Legal Reasons",
    "500 Internal Server Error",
    "501 Not Implemented",
    "502 Bad Gateway",
    "503 Service Unavailable",
    "504 Gateway Timeout",
    "505 HTTP Version Not Supported",
    "506 Variant Also Negotiates",
    "507 Insufficient Storage",
    "508 Loop Detected",
    "510 Not Extended",
    "511 Network Authentication Required",
]

rejected = [
    "Internal Server Error",
    "__NOEDITSECTION__",
    "enter your username and password",
    "forgotten your password",
    "cookies enabled",
    "enable JavaScript in your browser.",
    "The page cannot be displayed",
    "site or edit the error_page",
]

rejected.extend(http_errors)


def replace_multiple(input_string, pattern=r"\s{6,}", replace="   "):
    return re.sub(pattern, replace, input_string)


def replace(string):
    string = replace_multiple(string.replace("…", "."))
    string = replace_multiple(string, pattern=r"\.{6,}", replace="...")
    return string


def reject(string):
    if any([r in string for r in rejected]):
        return True
    return False


def loop(files, process_type="multi"):
    if process_type == "multi":
        files, _ = files

    for f in files:
        new_f = f.replace("dedupe-datasets/", "postprocessing/")
        new_f_done = f.replace("dedupe-datasets/", "postprocessing-done/")
        if os.path.exists(new_f_done):
            continue
        with open(new_f, "w") as fopen_l:
            with open(f) as fopen:
                for l in tqdm(fopen):
                    data = json.loads(l)

                    if reject(data["text"]):
                        continue

                    data = replace(data["text"].strip())

                    if len(data) < 3:
                        continue

                    fopen_l.write(f"{json.dumps(data)}\n")
                    fopen_l.flush()

        with open(new_f_done, "w") as fopen:
            fopen.write("done")
