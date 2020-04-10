import boto3
import os
import json


class AwsManager(object):

    bucket = os.environ.get("INPUT_BUCKET")

    def __init__(self):
        self.rekognition_client = boto3.client("rekognition", region_name="us-east-1")
        self.dynamo_client = boto3.resource("dynamodb")

    def compare_faces(self, source_img_url, target_img_url):

        max_similarity = 0
        try:
            response = self.rekognition_client.compare_faces(
                SimilarityThreshold=40,
                SourceImage={
                    "S3Object": {
                        "Bucket": self.bucket,
                        "Name": source_img_url
                    }
                },
                TargetImage={
                    "S3Object": {
                        "Bucket": self.bucket,
                        "Name": target_img_url
                    }
                }
            )
            for faceMatch in response["FaceMatches"]:
                confidence = str(faceMatch["Face"]["Confidence"])
                similarity = float(faceMatch["Similarity"])
                if similarity > max_similarity:
                    max_similarity = similarity

        except Exception as e:
            print(f"Failed to use file: {source_img_url} - {str(e)}")
            max_similarity = -1
            response = {}

        return max_similarity, response

    def to_dynamo(self, img_url, max_similarity, json_response):
        table = self.dynamo_client.Table(os.environ["DYNAMODB_TABLE"])

        item = {
            "img_url": str(img_url),
            "max_similarity": max_similarity,
            "response": json.dumps(json_response)
        }

        with table.batch_writer() as batch:
            batch.put_item(Item=item)
