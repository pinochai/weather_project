Weather Data Collection and API Service on AWS
This project is a serverless, event-driven weather data processing system built using AWS CDK (Python).
It fetches weather data automatically from the Open-Meteo API, stores it in DynamoDB and S3, sends notifications via SNS, and exposes a simple REST API using API Gateway.

🛠️ Architecture Overview
AWS Lambda:

fetch_lambda: Fetches weather data from Open-Meteo.

store_lambda: Stores fetched weather data into DynamoDB and S3, and sends SNS notifications.

AWS Step Functions: Orchestrates the fetch and store Lambda functions in sequence.

Amazon EventBridge: Triggers the Step Function every hour automatically.

Amazon DynamoDB: Stores structured weather data records.

Amazon S3: Stores raw weather data responses.

Amazon SNS: Sends email notifications after data is stored.

Amazon API Gateway: Exposes an HTTP API (GET /weather) to fetch live weather data on demand.

📂 Project Structure
graphql
Copy
Edit
├── cdk.json
├── README.md
├── lambda_package/
│   ├── fetch.py   # Lambda: Fetches weather data from Open-Meteo
│   └── store.py   # Lambda: Stores weather data into DynamoDB/S3 and sends SNS notification
├── stack/
│   └── weather_data_stack.py  # CDK Stack: All AWS resources and wiring
├── requirements.txt
└── ...
🚀 How the System Works
Automated Data Collection (Scheduled)
EventBridge triggers the Step Function every hour.

Step Function:

Fetch Lambda retrieves live weather data from Open-Meteo API.

Store Lambda saves the weather data into DynamoDB and S3, and sends a notification email via SNS.

On-Demand API Access
Call the API endpoint:

plaintext
Copy
Edit
GET /weather?latitude=35.8245&longitude=10.6346
API Gateway triggers fetch_lambda to fetch live weather for the specified location (defaults to Sousse, Tunisia if not provided).

⚙️ Features
✅ Serverless architecture (Lambda, DynamoDB, S3, Step Functions)

✅ Hourly automated fetch using EventBridge and Step Functions

✅ Weather data storage in DynamoDB (structured) and S3 (raw)

✅ Email notifications via SNS after storing data

✅ Public REST API to fetch weather data live

✅ IAM permissions tightly managed (SNS publish access for Lambda only)

✅ Resource cleanup (DynamoDB, S3 auto-deleted in dev environments)

✅ SSL warnings handled when fetching external API

📧 Notifications
Email Address Subscribed:
mehdi.sghaier@draexlmaier.com

Trigger:
After successful storage of weather data (by the store Lambda).

📈 Monitoring & Alerts
CloudWatch Logs enabled for all Lambda functions and Step Functions for easy debugging.

🔧 Environment Variables for Lambdas

Lambda	Environment Variables	Description
store_lambda	TABLE_NAME (DynamoDB table)	Where weather data is stored
BUCKET_NAME (S3 bucket)	Where raw weather data is saved
TOPIC_ARN (SNS topic)	For sending notification emails
🧹 Resource Cleanup
When the stack is destroyed:

DynamoDB table and S3 bucket are deleted (in dev/testing).

In production, you can easily update the removal_policy to RETAIN.

🧪 How to Deploy
Install AWS CDK if you haven't:

bash
Copy
Edit
npm install -g aws-cdk
Install Python dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Bootstrap your AWS environment:

bash
Copy
Edit
cdk bootstrap
Deploy the stack:

bash
Copy
Edit
cdk deploy WeatherDataStack-dev
🌍 Open-Meteo API
The external weather service used:

Base URL: https://api.open-meteo.com/v1/forecast

Parameters: latitude, longitude, hourly=temperature_2m

SSL verification is disabled for testing (can be safely enabled in production).

🙌 Author
Mehdi Sghaier