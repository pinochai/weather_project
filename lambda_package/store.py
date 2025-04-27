import json
import boto3
import uuid
from datetime import datetime
import os
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']  # Ensure environment variable is set correctly
table = dynamodb.Table(table_name)

# Initialize S3 client
s3_client = boto3.client('s3')
bucket_name = os.environ['BUCKET_NAME']

# Initialize SNS client
sns_client = boto3.client('sns')
topic_arn = os.environ['TOPIC_ARN']


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError

def lambda_handler(event, context):
    print("📩 Received event:", json.dumps(event, indent=2))  # Debugging

    try:
        # Ensure event contains weather_data.Payload.body
        if "weather_data" not in event or "Payload" not in event["weather_data"] or "body" not in event["weather_data"]["Payload"]:
            raise ValueError("Missing 'weather_data.Payload.body' in event.")

        # Parse event to get weather data
        weather_data = json.loads(event["weather_data"]["Payload"]["body"])
        print("🌤 Parsed Weather Data:", json.dumps(weather_data, indent=2))  # Debugging

        # Extract temperature 
        temperature = Decimal(str(weather_data["hourly"]["temperature_2m"][0]))  # Convert to Decimal
        timestamp = datetime.utcnow().isoformat()

        # Generate unique ID
        record_id = str(uuid.uuid4())

        # Construct item for DynamoDB
        item = {
            "record_id": record_id,  # Use 'record_id' as the key
            "timestamp": timestamp,
            "temperature": temperature,
            "latitude": Decimal(str(weather_data.get("latitude"))),
            "longitude": Decimal(str(weather_data.get("longitude"))),
        }

        print("📝 Storing item in DynamoDB:", json.dumps(item, indent=2, default=decimal_default))  # Debugging

        # Store data in DynamoDB
        response = table.put_item(Item=item)
        print("✅ DynamoDB Response:", response)  # Debugging

        # Save data to S3
        s3_key = f"weather_data/{record_id}.json"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=json.dumps(item, default=decimal_default),
            ContentType='application/json'
        )
        print(f"✅ Data saved to S3: {s3_key}")


        # Publish a message to SNS Topic
        sns_message = {
            "message": "New weather data stored",
            "record_id": record_id,
            "timestamp": timestamp,
            "temperature": str(temperature),
            "latitude": str(item["latitude"]),
            "longitude": str(item["longitude"])
        }
        sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(sns_message, default=decimal_default),
            Subject="New Weather Data Notification"
        )


        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data stored successfully!", "record_id": record_id})
        }

    except Exception as e:
        print("❌ Error:", str(e))  # Debugging
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}, default=decimal_default)  # Convert Decimal to str for JSON serialization
        }