import json

from lib.aws_manager import AwsManager

aws_manager = AwsManager()


def lambda_handler(event, context):
    print(event)
    img_url = json.loads(event["Records"][0]["body"])["img_url"]

    print("Start comparing faces")

    max_similarity, json_result = aws_manager.compare_faces(img_url)

    body = {"img_url": img_url, "max_similarity": int(max_similarity)}

    aws_manager.to_dynamo(img_url, int(max_similarity), json_result)

    print("Finished comparing faces.")
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        },
        "body": json.dumps(body)
    }


if __name__ == "__main__":
    event = {u"Records": [{"body": "{'img_url':'submissions/uploads/yvette.saint@hotmail.com/61304/900/647.jpg'}",
                           u"receiptHandle": u"AQEBcz6CwGhsb924ggPHwD+ZmwaIOndJTUJqHywpfBqGT0NTQHlBFlhsNDfRsAdWEpXELS8cT02S3b15nBmhExA2cQtPzxSYB6keE2zB6SKnaRlanMZk/d30MwKD7dTcYLTpK8AQB9+mNIntPm3CR/iLaiAurEqPi81vn0CtjL3KSFL5Y/4p9uf5gon9zFrkqqY0tVfXOTjoitaN13a7mJkGuZSH+B+oERJDwow//lyFGKdV6pEdSOMfnFnIUYdQiIAaSv6NMlrPwGkC+o2fYx2mTESFhDuzDhmXgXxXgqBfIAyjGWi3k45rvEDVnbYvYUQ4BJDDsZ+LgwBh/Kbqzecf9Ij2588AzeBDv7XtUUrN8WPzfK074gdmGwNfODCYvdP2ycG+NCCn2FeKYfQ3w46bMg==",
                           u"md5OfBody": u"f228a274a15e4b42931072f987ac5a4c",
                           u"eventSourceARN": u"arn:aws:sqs:eu-central-1:788272471874:FaceCompareQueue",
                           u"eventSource": u"aws:sqs", u"awsRegion": u"eu-central-1",
                           u"messageId": u"2f709ea6-0446-48b4-a0f2-e2b02270d728",
                           u"attributes": {u"ApproximateFirstReceiveTimestamp": u"1547502029020",
                                           u"SenderId": u"788272471874",
                                           u"ApproximateReceiveCount": u"28", u"SentTimestamp": u"1547502029020"},
                           u"messageAttributes": {}}]}

    event = json.dumps(event)
    print(lambda_handler(event, context=None))
