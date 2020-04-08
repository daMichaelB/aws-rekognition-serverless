import json

from lib.aws_manager import AwsManager

aws_manager = AwsManager()


def lambda_handler(event, context):
    for record in event["Records"]:
        img_url = json.loads(record["body"])["img_url"]

        print(f"Start comparing faces for {img_url}")
        max_similarity, json_result = aws_manager.compare_faces(img_url)
        aws_manager.to_dynamo(img_url, int(max_similarity), json_result)
        print("Finished comparing faces.")


if __name__ == "__main__":
    event = {u"Records": [{"body": "{'img_url': 'key_of_image1.jpg'}"}]}
    print(lambda_handler(event, context=None))
