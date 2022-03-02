import csv
import os

import boto3
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

AWS_ID = os.getenv("AWS_ID")
AWS_KEY = os.getenv("AWS_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")

# boto3.setup_default_session(region_name=region)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ID,
    aws_secret_access_key=AWS_KEY,
)


def download_dir(fileName, local, bucket, client=s3_client):
    """
    params:
    - prefix: pattern to match in s3
    - local: local path to folder in which to place files
    - bucket: s3 bucket with target contents
    - client: initialized s3 client object
    """
    print("starting")
    keys = []
    dirs = []
    next_token = ""
    base_kwargs = {
        "Bucket": bucket,
        "Prefix": fileName,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != "":
            kwargs.update({"ContinuationToken": next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get("Contents")
        for i in contents:
            k = i.get("Key")
            if k[-1] != "/":
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get("NextContinuationToken")
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        client.download_file(bucket, k, dest_pathname)


invpath = r"/home/rian/Python_scripts/env_s3_downloader/pdf_list.csv"
files_ = []

with open(invpath) as f:
    readCSV = csv.reader(f)
    for row in readCSV:
        files_.extend(row)

outpath = r"/home/rian/Python_scripts/env_s3_downloader/envelopes"
bucket = BUCKET_NAME


def get_files():
    for f in tqdm(files_):
        download_dir(f, outpath, bucket, s3_client)


if __name__ == "__main__":
    get_files()
