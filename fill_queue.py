import json
import os

import boto3

sqs = boto3.resource("sqs", region_name="eu-central-1")
queue = sqs.get_queue_by_name(QueueName=os.environ.get("QUEUE_NAME"))

image_file_list = "demo/s3_image_list.txt"
target_file = "target.jpg"
with open(image_file_list, "r") as f:
    for line in f:
        source_file = line.strip()
        print(f"Sending to Queue {source_file}")
        try:
            queue.send_message(MessageBody=(json.dumps({"img_url": source_file, "target_img_url": target_file})))

        except Exception as e:
            print(f"Failed to use file: {source_file} {str(e)}")
