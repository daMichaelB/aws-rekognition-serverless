# AWS Rekognition Serverless

This lambda function will use Rekognition to detect a specific person on thousands of images.

> Due to the serverless approach thousands of images can be processed at the same time.

We will create a lambda function / SQS Queue / DynamoDB and IAM Roles.

## Prerequisites

* AWS Account
* A S3 bucket containing all your images
* A S3 bucket (can be the same) that contains an image of the target person.

## Deploy function:

First deploy the **Serverless** stack into your AWS account:

```bash
export INPUT_BUCKET='your-bucket-name'
serverless deploy -v
```

## Trigger Lambda

Put this item into the SQS queue to trigger the lambda function:

```bash
{"img_url": "images/image1.jpg", "target_img_url": "target.jpg"}
```

You can already use the `fill_queue.py` script to automatically add all images from a `.txt` file into that queue.

The results will directly be stored into a Dynamo-DB.

## Remove stack
```bash
serverless remove
```
