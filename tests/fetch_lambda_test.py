import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lambda_function')))
from fetch import lambda_handler

# Mock event with query parameters for testing locally
event = {
    "queryStringParameters": {
        "latitude": "35.6895",
        "longitude": "139.6917"
    }
}

context = None  # Mock context (can be empty if not needed)
result = lambda_handler(event, context)
print(result)

