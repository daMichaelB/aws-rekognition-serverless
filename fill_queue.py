import json
import os

import boto3

inline_counter = 0
target_count = 0
endings_counter = 0
target_file = "targeted-refactored-images.txt"

file = open(target_file, "r")

for i in range(1, 1000):
    sourceFile = file.readline().strip()
    print(f"{i}: Sending to Queue {sourceFile}")
    try:
        sqs = boto3.client("sqs")

        queue_name = os.environ.get("QUEUE_NAME")
        #TODO: queue_url = get_queue_by_name(queue_name)
        queue_url = "SOME-QUEUE-URL"

        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=(
                json.dumps({"img_url": sourceFile})
            )
        )

        print(response["MessageId"])

    except Exception as e:
        print(f"Failed to use file: {sourceFile} {str(e)}")
