import os
import json
import boto3
from playwright.sync_api import sync_playwright


COSTCO_LOGIN_URL = "https://www.costco.com/LogonForm"
GOLD_BARS_URL = "https://www.costco.com/gold-bars.html"


def get_credentials():
    """Retrieve Costco credentials from AWS Secrets Manager."""
    secret_name = os.environ.get("COSTCO_SECRET_NAME", "costco-alerting-service/credentials")
    region = os.environ.get("AWS_REGION", "us-west-2")
    
    client = boto3.client("secretsmanager", region_name=region)
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    
    return secret["username"], secret["password"]


def check_gold_bars_availability():
    """
    Login to Costco and check if 1oz gold bars are available.
    Returns a dict with availability info.
    """
    username, password = get_credentials()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            page.goto(COSTCO_LOGIN_URL, wait_until="networkidle")
            page.fill("#signInName", username)
            page.fill("#password", password)
            page.click("#logonButton")
            page.wait_for_load_state("networkidle")
            
            page.goto(GOLD_BARS_URL, wait_until="networkidle")
            page.wait_for_selector(".product-tile", timeout=10000)
            
            products = page.query_selector_all(".product-tile")
            available_gold_bars = []
            
            for product in products:
                title_elem = product.query_selector(".description")
                price_elem = product.query_selector(".price")
                add_to_cart = product.query_selector("[data-testid='add-to-cart-button']")
                
                if title_elem:
                    title = title_elem.inner_text().lower()
                    if "1 oz" in title or "1oz" in title:
                        is_available = add_to_cart is not None and add_to_cart.is_visible()
                        price = price_elem.inner_text() if price_elem else "Price unavailable"
                        
                        if is_available:
                            available_gold_bars.append({
                                "title": title_elem.inner_text(),
                                "price": price,
                                "available": True
                            })
            
            return {
                "checked": True,
                "available_count": len(available_gold_bars),
                "products": available_gold_bars
            }
            
        except Exception as e:
            return {
                "checked": False,
                "error": str(e),
                "available_count": 0,
                "products": []
            }
        finally:
            browser.close()
