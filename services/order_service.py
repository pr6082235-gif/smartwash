"""Order service functions"""
import random
import string
from datetime import datetime
import os


def generate_order_id():
    """Generate unique order ID like SW-2024-XXXXX"""
    year = datetime.now().year
    random_part = ''.join(random.choices(string.digits, k=5))
    return f"SW-{year}-{random_part}"


def generate_barcode(order_id):
    """Generate unique barcode string"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"SWP{timestamp}{order_id.replace('-', '')}"


def calculate_price(service_type, quantity):
    """Base price calculation"""
    base_prices = {
        'wash': 35,
        'dry_clean': 120,
        'iron': 18,
        'wash_iron': 50,
        'dry_clean_iron': 140,
    }
    base = base_prices.get(service_type, 35)
    return base * quantity


def generate_barcode_image(barcode_text, output_path):
    """Generate barcode image file"""
    try:
        import barcode
        from barcode.writer import ImageWriter
        
        code128 = barcode.get_barcode_class('code128')
        bc = code128(barcode_text, writer=ImageWriter())
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        filename = bc.save(output_path.replace('.png', ''))
        return filename
    except Exception as e:
        print(f"Barcode generation error: {e}")
        return None
