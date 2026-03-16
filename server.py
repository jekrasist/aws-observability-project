import logging
import uuid
import time
from flask import Flask, jsonify
import boto3
from botocore.exceptions import NoCredentialsError

# 1. Setup Structured Logging (JSON-like)
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s", "level": "%(levelname)s", "correlation_id": "%(message)s"}',
    handlers=[logging.FileHandler("/tmp/app.log"), logging.StreamHandler()]
)

app = Flask(__name__)
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1') # Ensure this matches your region

@app.route('/order', methods=['GET'])
def place_order():
    correlation_id = str(uuid.uuid4())
    
    # Log the event
    logging.info(correlation_id)

    # 2. Push Custom Metric to CloudWatch
    try:
        cloudwatch.put_metric_data(
            Namespace='CloudServiceProject',
            MetricData=[{
                'MetricName': 'SuccessfulOrders',
                'Value': 1,
                'Unit': 'Count'
            }]
        )
    except Exception as e:
        print(f"Error sending metric: {e}")

    return jsonify({
        "status": "order_placed",
        "id": correlation_id
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
