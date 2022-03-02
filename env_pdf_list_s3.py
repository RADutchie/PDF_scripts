import csv
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

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

allowedFileTypes = "pdf"
awsRegion = "ap-southeast-2"


def getFiles(s3client=s3_client, bucketName=BUCKET_NAME):
    print("start get files")

    files = []

    # currentPage = 1
    hasMoreContent = True
    continuationToken = None

    while hasMoreContent:
        if continuationToken:
            listObjectsResponse = s3client.list_objects_v2(
                Bucket=bucketName, ContinuationToken=continuationToken
            )
        else:
            listObjectsResponse = s3client.list_objects_v2(Bucket=bucketName)

        if listObjectsResponse["IsTruncated"]:
            continuationToken = listObjectsResponse["NextContinuationToken"]
        else:
            hasMoreContent = False

        for doc in listObjectsResponse["Contents"]:
            docName = doc["Key"]
            files.append([docName])
    print("get files return: {}files {}".format(len(files), files[0]))

    cwd = Path.cwd()

    with open(cwd / "envelope_list.csv", "w") as e:
        writer = csv.writer(e)
        writer.writerows(files)


if __name__ == "__main__":
    getFiles()
