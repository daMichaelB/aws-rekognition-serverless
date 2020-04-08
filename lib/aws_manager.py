import boto3
import os
import json


class AwsManager(object):

    bucket = os.environ.get("INPUT_BUCKET")

    def compare_faces(self, img_url):

        client = boto3.client("rekognition", region_name="us-east-1")

        print(f"Sending to Rekognition {img_url}")
        max_similarity = 0
        try:
            response = client.compare_faces(SimilarityThreshold=40,
                                            SourceImage={
                                                "S3Object": {
                                                    "Bucket": self.bucket,
                                                    "Name": img_url
                                                }
                                            },
                                            TargetImage={
                                                "S3Object": {
                                                    "Bucket": self.bucket,
                                                    "Name": "findthisguy2.jpg"
                                                }
                                            })
            for faceMatch in response["FaceMatches"]:
                # position = faceMatch["Face"]["BoundingBox"]
                confidence = str(faceMatch["Face"]["Confidence"])
                similarity = float(faceMatch["Similarity"])
                if similarity > max_similarity:
                    max_similarity = similarity

        except Exception as e:
            print(f"Failed to use file: {img_url} - {str(e)}")
            max_similarity = -1
            response = {}

        return max_similarity, response

    @staticmethod
    def to_dynamo(img_url, max_similarity, json_response):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

        print(max_similarity)

        item = {
            "img_url": str(img_url),
            "max_similarity": max_similarity,
            "response": json.dumps(json_response)
        }
        # put items with batch-writer. this will handle unprocessed items (dynamodb was overloaded) and resend them
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
