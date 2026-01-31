# Costco Gold Bar Alerting Service

Monitors Costco for 1oz gold bar availability and sends SMS alerts when in stock.

## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS SAM CLI installed
- Python 3.11+

## Setup

### 1. Store Costco Credentials in AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name costco-alerting-service/credentials \
  --secret-string '{"username":"your-costco-email","password":"your-costco-password"}'
```

### 2. Deploy

```bash
sam build
sam deploy --guided
```

During deployment, provide:
- `PhoneNumber`: Your phone number in E.164 format (e.g., +14155551234)

## Local Testing

```bash
pip install -r requirements.txt
playwright install chromium

# Set environment variables
export PHONE_NUMBER=+14155551234
export AWS_REGION=us-west-2

# Run locally
python src/handler.py
```

## Architecture

- **AWS Lambda**: Runs the checker every 15 minutes
- **EventBridge**: Schedules Lambda execution
- **Secrets Manager**: Stores Costco credentials securely
- **SNS**: Sends SMS alerts

## Note

This service uses browser automation to check Costco. For Lambda deployment, you may need to use a Lambda layer with Chromium (e.g., `chrome-aws-lambda`) or consider using AWS Fargate for more complex browser automation needs.
