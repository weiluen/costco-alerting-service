import json
import logging
from costco_checker import check_gold_bars_availability
from notifier import send_sms_alert

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler - checks Costco for 1oz gold bar availability
    and sends email alert if found.
    """
    logger.info("Starting Costco gold bar availability check")
    
    try:
        result = check_gold_bars_availability()
        
        if not result["checked"]:
            logger.error(f"Failed to check availability: {result.get('error')}")
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "message": "Failed to check availability",
                    "error": result.get("error")
                })
            }
        
        if result["available_count"] > 0:
            logger.info(f"Found {result['available_count']} available 1oz gold bars!")
            
            sms_result = send_sms_alert(result["products"])
            
            if sms_result["success"]:
                logger.info(f"Alert SMS sent successfully: {sms_result['message_id']}")
            else:
                logger.error(f"Failed to send SMS: {sms_result['error']}")
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Gold bars available! Alert sent.",
                    "products": result["products"],
                    "sms_sent": sms_result["success"]
                })
            }
        else:
            logger.info("No 1oz gold bars currently available")
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "No 1oz gold bars available",
                    "products": []
                })
            }
            
    except Exception as e:
        logger.exception("Unexpected error in lambda handler")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Unexpected error",
                "error": str(e)
            })
        }
