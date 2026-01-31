# Agentic Plan for Costco Alerting Service

## Overview
A service that monitors Costco's website for 1oz gold bar availability and sends email alerts when in stock.

## Goals
- Authenticate with Costco using user credentials
- Monitor the gold bars product page for 1oz variety availability
- Send email notifications when gold bars are in stock
- Deploy to AWS for scheduled execution

## Architecture
- **Runtime**: AWS Lambda (Python 3.11)
- **Scheduling**: Amazon EventBridge (runs every 15 minutes)
- **Notifications**: Amazon SNS for SMS alerts
- **Secrets**: AWS Secrets Manager for credentials
- **Browser Automation**: Playwright for headless browser login/scraping

## Components
- `handler.py` - Lambda entry point
- `costco_checker.py` - Costco login and product checking logic
- `notifier.py` - SMS notification via SNS
- `requirements.txt` - Python dependencies
- `template.yaml` - AWS SAM deployment template

## Implementation Plan
1. Create Python scraping logic with Playwright
2. Implement SMS notification via AWS SNS
3. Create AWS SAM template for Lambda deployment
4. Configure EventBridge for scheduled execution
5. Store credentials securely in Secrets Manager

## Security Considerations
- Credentials stored in AWS Secrets Manager (never in code)
- Lambda runs in VPC if needed
- IAM roles with least privilege
