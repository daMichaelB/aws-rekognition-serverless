# AWS Rekognition Serverless

This lambda function will use Rekognition to detect a specific person on thousands of images

The serverless framework creates a lambda function / SQS Queue / DynamoDB and IAM Roles.

## Deploy function:

```bash
serverless deploy -v
```

## Remove stack
```bash
serverless remove
```

## Trigger Lambda

Put this item into the SQS queue to start the lambda function:

```bash
{"img_url": "path_to_s3_file"}
```
