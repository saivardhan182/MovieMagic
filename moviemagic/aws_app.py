import boto3
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Initialize SNS client
sns_client = boto3.client(
    'sns',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Your SNS topic ARN (from AWS Console)
sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

# ✅ Function to store booking in DynamoDB
def store_in_dynamodb(data):
    try:
        table = dynamodb.Table('Bookings')  # Make sure you create this table in AWS
        item = data.copy()
        item['timestamp'] = int(time.time())
        table.put_item(Item=item)
        print("✅ Booking stored in DynamoDB")
    except Exception as e:
        print("❌ DynamoDB Error:", e)

# ✅ Function to send SNS notification
def send_sns_notification(data):
    try:
        message = f"""
New Booking Confirmed! 🎬

Name: {data['name']}
Movie: {data['movie']}
Date: {data['date']}
Time: {data['time']}
Seats: {data['seats']}
Email: {data['email']}
"""
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject='🎉 MovieMagic Booking Confirmed!'
        )
        print("✅ SNS notification sent")
    except Exception as e:
        print("❌ SNS Error:", e)
