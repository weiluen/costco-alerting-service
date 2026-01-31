import os
import boto3
from botocore.exceptions import ClientError


def send_sms_alert(products: list):
    """Send SMS notification via AWS SNS when gold bars are available."""
    phone_number = os.environ.get("PHONE_NUMBER")
    region = os.environ.get("AWS_REGION", "us-west-2")
    
    if not phone_number:
        raise ValueError("PHONE_NUMBER environment variable must be set")
    
    product_list = ", ".join([f"{p['title']}: {p['price']}" for p in products])
    
    message = f"🏅 Costco 1oz Gold Bars Available! {len(products)} in stock. {product_list[:100]}... Check: costco.com/gold-bars.html"
    
    if len(message) > 160:
        message = f"🏅 Costco 1oz Gold Bars Available! {len(products)} in stock. Check: costco.com/gold-bars.html"
    
    client = boto3.client("sns", region_name=region)
    
    try:
        response = client.publish(
            PhoneNumber=phone_number,
            Message=message,
            MessageAttributes={
                "AWS.SNS.SMS.SMSType": {
                    "DataType": "String",
                    "StringValue": "Transactional"
                }
            }
        )
        return {"success": True, "message_id": response["MessageId"]}
    except ClientError as e:
        return {"success": False, "error": e.response["Error"]["Message"]}
