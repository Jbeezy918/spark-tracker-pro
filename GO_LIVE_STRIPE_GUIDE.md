# 🚀 Spark Tracker - Go LIVE with Stripe

## Step 1: Get Your LIVE Stripe Keys

1. Go to https://dashboard.stripe.com
2. Toggle the **"Test mode"** switch in the top right to OFF (LIVE mode)
3. Click **"Developers"** → **"API keys"**
4. Copy these two keys:
   - **Publishable key**: Starts with `pk_live_...`
   - **Secret key**: Starts with `sk_live_...` (click "Reveal" to see it)

## Step 2: Create LIVE Products & Prices

### Create Basic Tier Product:
1. Go to **Products** → **"+ Add product"**
2. Fill in:
   - **Name**: Spark Tracker Basic
   - **Description**: Unlimited trips, 1.5 years data, 15 themes, voice keywords
   - **Pricing**: $6.99 USD / month (recurring)
   - **Tax code**: Software as a Service (SaaS)
3. Click **Save product**
4. Copy the **Price ID** (starts with `price_...`)

### Create Pro Tier Product:
1. Click **"+ Add product"** again
2. Fill in:
   - **Name**: Spark Tracker Pro
   - **Description**: Everything + 30 themes, conversational AI, screen capture, 2 years data
   - **Pricing**: $9.99 USD / month (recurring)
   - **Tax code**: Software as a Service (SaaS)
3. Click **Save product**
4. Copy the **Price ID** (starts with `price_...`)

## Step 3: Create Payment Links

### Basic Tier Payment Link:
1. Go to **Payment links** → **"+ New"**
2. Select the **Spark Tracker Basic** product
3. Enable **"Collect customer's billing address"**
4. Enable **"Allow promotion codes"**
5. Set **Success URL**: `https://spark-tracker-pro.streamlit.app/?payment_success=true&tier=basic`
6. Click **Create link**
7. Copy the payment link URL

### Pro Tier Payment Link:
1. Click **"+ New"** again
2. Select the **Spark Tracker Pro** product
3. Same settings as above
4. Set **Success URL**: `https://spark-tracker-pro.streamlit.app/?payment_success=true&tier=pro`
5. Click **Create link**
6. Copy the payment link URL

## Step 4: Set Up Webhook Endpoint

1. Go to **Developers** → **Webhooks** → **"+ Add endpoint"**
2. **Endpoint URL**: `https://spark-tracker-webhook.your-domain.com/stripe-webhook`
   - (We'll set this up in Step 5)
3. **Events to listen to**:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
4. Click **Add endpoint**
5. Copy the **Signing secret** (starts with `whsec_...`)

## Step 5: Update Streamlit Secrets

In Streamlit Cloud dashboard:

1. Go to https://share.streamlit.io/
2. Find your **spark-tracker-pro** app
3. Click **Settings** (⚙️) → **Secrets**
4. Replace with your LIVE keys:

```toml
# Stripe LIVE MODE Configuration
STRIPE_PUBLISHABLE_KEY = "pk_live_YOUR_KEY_HERE"
STRIPE_SECRET_KEY = "sk_live_YOUR_KEY_HERE"

# LIVE Price IDs
BASIC_PRICE_ID = "price_YOUR_BASIC_ID"
PRO_PRICE_ID = "price_YOUR_PRO_ID"

# LIVE Payment Links
BASIC_PAYMENT_LINK = "https://buy.stripe.com/YOUR_BASIC_LINK"
PRO_PAYMENT_LINK = "https://buy.stripe.com/YOUR_PRO_LINK"

# Webhook Secret
STRIPE_WEBHOOK_SECRET = "whsec_YOUR_WEBHOOK_SECRET"
```

## Step 6: What We'll Update in Code

I'll update these files to support LIVE mode:
- `spark_app.py` - Add payment success handling
- `stripe_integration.py` - Update pricing to $6.99/$9.99
- Add webhook handler for subscription activation

## Step 7: Test Before Going Fully Live

1. Use Stripe's **Test Clock** feature to test subscription lifecycle
2. Make a test purchase with a real card in LIVE mode (you can refund it)
3. Verify webhook events are being received
4. Test the upgrade flow from Free → Basic → Pro

## Pricing Summary

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | 10 trips/week, 7 days data, 5 themes |
| **Basic** | $6.99/mo | Unlimited trips, 1.5 years data, 15 themes, voice |
| **Pro** | $9.99/mo | Everything + 30 themes, AI, screen capture, 2 years |

## Ready to Go Live?

Once you have:
- ✅ LIVE Publishable key
- ✅ LIVE Secret key
- ✅ Basic Price ID
- ✅ Pro Price ID
- ✅ Basic Payment Link
- ✅ Pro Payment Link
- ✅ Webhook Secret

...share them with me and I'll update the code and deploy! 🚀

## Security Notes

- Never share your SECRET key publicly
- Webhook signature verification is CRITICAL (prevents fraud)
- Always use HTTPS for webhook endpoints
- Store keys in Streamlit Secrets (encrypted at rest)
