#!/usr/bin/env python3
"""
Setup Stripe products and prices for Spark Tracker Pro
"""
import stripe
import os

# Get API key from environment or use provided key
import sys

if len(sys.argv) > 1:
    STRIPE_SECRET = sys.argv[1]
else:
    STRIPE_SECRET = os.getenv("STRIPE_SECRET", "")

if not STRIPE_SECRET:
    print("❌ Error: No Stripe API key provided")
    print("Usage: python3 setup_stripe.py <stripe_secret_key>")
    sys.exit(1)

stripe.api_key = STRIPE_SECRET

def setup_products_and_prices():
    """Create or verify Stripe products and prices"""

    print("🔍 Checking existing products...")

    # List existing products
    products = stripe.Product.list(limit=100)

    regular_product = None
    pro_product = None

    # Check if products already exist
    for product in products.data:
        if product.name == "Spark Tracker - Regular":
            regular_product = product
            print(f"✓ Found Regular product: {product.id}")
        elif product.name == "Spark Tracker - Pro":
            pro_product = product
            print(f"✓ Found Pro product: {product.id}")

    # Create Regular product if it doesn't exist
    if not regular_product:
        print("\n📦 Creating Regular product...")
        regular_product = stripe.Product.create(
            name="Spark Tracker - Regular",
            description="Track trips and earnings with essential features",
        )
        print(f"✓ Created Regular product: {regular_product.id}")

    # Create Pro product if it doesn't exist
    if not pro_product:
        print("\n📦 Creating Pro product...")
        pro_product = stripe.Product.create(
            name="Spark Tracker - Pro",
            description="Advanced analytics, unlimited trips, and premium features",
        )
        print(f"✓ Created Pro product: {pro_product.id}")

    # Check existing prices
    print("\n🔍 Checking existing prices...")
    prices = stripe.Price.list(limit=100)

    regular_price = None
    pro_price = None

    for price in prices.data:
        if price.product == regular_product.id and price.unit_amount == 399:
            regular_price = price
            print(f"✓ Found Regular price: {price.id} ($3.99/mo)")
        elif price.product == pro_product.id and price.unit_amount == 699:
            pro_price = price
            print(f"✓ Found Pro price: {price.id} ($6.99/mo)")

    # Create Regular price if it doesn't exist
    if not regular_price:
        print("\n💰 Creating Regular price ($3.99/mo)...")
        regular_price = stripe.Price.create(
            product=regular_product.id,
            unit_amount=399,  # $3.99
            currency="usd",
            recurring={"interval": "month"},
        )
        print(f"✓ Created Regular price: {regular_price.id}")

    # Create Pro price if it doesn't exist
    if not pro_price:
        print("\n💰 Creating Pro price ($6.99/mo)...")
        pro_price = stripe.Price.create(
            product=pro_product.id,
            unit_amount=699,  # $6.99
            currency="usd",
            recurring={"interval": "month"},
        )
        print(f"✓ Created Pro price: {pro_price.id}")

    print("\n" + "="*60)
    print("✅ STRIPE SETUP COMPLETE")
    print("="*60)
    print(f"\nRegular Plan: {regular_product.name}")
    print(f"  Product ID: {regular_product.id}")
    print(f"  Price ID: {regular_price.id}")
    print(f"  Amount: ${regular_price.unit_amount/100:.2f}/mo")

    print(f"\nPro Plan: {pro_product.name}")
    print(f"  Product ID: {pro_product.id}")
    print(f"  Price ID: {pro_price.id}")
    print(f"  Amount: ${pro_price.unit_amount/100:.2f}/mo")

    return {
        "regular_price_id": regular_price.id,
        "pro_price_id": pro_price.id,
    }

if __name__ == "__main__":
    result = setup_products_and_prices()

    print("\n" + "="*60)
    print("📋 ADD THESE TO YOUR .streamlit/secrets.toml:")
    print("="*60)
    print(f'REGULAR_PRICE_ID = "{result["regular_price_id"]}"')
    print(f'PRO_PRICE_ID = "{result["pro_price_id"]}"')
