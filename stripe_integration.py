#!/usr/bin/env python3
"""
Stripe Payment Integration for Spark Tracker
Handles $12/mo Pro subscriptions with webhook processing
Built by Chlo - SavvyTech Automations
"""

import os
import stripe
import json
from datetime import datetime
from typing import Dict, Optional

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_demo_key_replace_with_real")

class SparkPaymentProcessor:
    """Handles all Stripe payment operations for Spark Tracker"""

    PRICE_PRO_MONTHLY = 1200  # $12.00 in cents
    PRICE_FLEET_MONTHLY = 3900  # $39.00 in cents

    def __init__(self):
        self.currency = "usd"

    def create_checkout_session(
        self,
        customer_email: str,
        tier: str = "pro",
        success_url: str = "https://savvytechautomations.com/success",
        cancel_url: str = "https://savvytechautomations.com/pricing"
    ) -> Dict:
        """
        Create a Stripe Checkout session for subscription

        Args:
            customer_email: User's email address
            tier: "pro" or "fleet"
            success_url: Where to redirect on successful payment
            cancel_url: Where to redirect if user cancels

        Returns:
            Dict with checkout session URL and session ID
        """
        try:
            # Determine price based on tier
            price = self.PRICE_PRO_MONTHLY if tier == "pro" else self.PRICE_FLEET_MONTHLY
            tier_name = "Pro Driver" if tier == "pro" else "Fleet Master"

            # Create Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': self.currency,
                        'product_data': {
                            'name': f'Spark Tracker {tier_name}',
                            'description': f'Monthly subscription to Spark Tracker {tier_name} tier',
                        },
                        'unit_amount': price,
                        'recurring': {
                            'interval': 'month',
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=success_url + f'?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=cancel_url,
                customer_email=customer_email,
                allow_promotion_codes=True,  # Enable discount codes
                billing_address_collection='auto',
                metadata={
                    'tier': tier,
                    'product': 'spark_tracker',
                    'created_at': datetime.utcnow().isoformat()
                }
            )

            return {
                'success': True,
                'checkout_url': session.url,
                'session_id': session.id
            }

        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def create_customer_portal_session(
        self,
        customer_id: str,
        return_url: str = "https://savvytechautomations.com/dashboard"
    ) -> Dict:
        """
        Create a Customer Portal session for managing subscription

        Args:
            customer_id: Stripe customer ID
            return_url: Where to return after portal actions

        Returns:
            Dict with portal URL
        """
        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=return_url,
            )

            return {
                'success': True,
                'portal_url': session.url
            }

        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }

    def handle_webhook_event(self, payload: bytes, sig_header: str) -> Dict:
        """
        Process Stripe webhook events

        Args:
            payload: Raw request body
            sig_header: Stripe signature header

        Returns:
            Dict with processing result
        """
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_demo")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError:
            return {'success': False, 'error': 'Invalid payload'}
        except stripe.error.SignatureVerificationError:
            return {'success': False, 'error': 'Invalid signature'}

        # Handle different event types
        event_type = event['type']
        event_data = event['data']['object']

        if event_type == 'checkout.session.completed':
            # Payment successful, activate subscription
            return self._handle_checkout_completed(event_data)

        elif event_type == 'customer.subscription.updated':
            # Subscription changed (upgrade/downgrade)
            return self._handle_subscription_updated(event_data)

        elif event_type == 'customer.subscription.deleted':
            # Subscription cancelled
            return self._handle_subscription_cancelled(event_data)

        elif event_type == 'invoice.payment_failed':
            # Payment failed, send reminder
            return self._handle_payment_failed(event_data)

        return {'success': True, 'event_type': event_type}

    def _handle_checkout_completed(self, session: Dict) -> Dict:
        """Handle successful checkout"""
        customer_email = session.get('customer_email')
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')

        # TODO: Update database - mark user as Pro tier
        # This will be connected to Supabase in next iteration

        print(f"✅ Subscription activated: {customer_email}")
        print(f"   Customer ID: {customer_id}")
        print(f"   Subscription ID: {subscription_id}")

        return {
            'success': True,
            'action': 'activate_subscription',
            'customer_email': customer_email,
            'customer_id': customer_id,
            'subscription_id': subscription_id
        }

    def _handle_subscription_updated(self, subscription: Dict) -> Dict:
        """Handle subscription updates"""
        customer_id = subscription.get('customer')
        status = subscription.get('status')

        print(f"📝 Subscription updated: {customer_id} -> {status}")

        return {
            'success': True,
            'action': 'update_subscription',
            'customer_id': customer_id,
            'status': status
        }

    def _handle_subscription_cancelled(self, subscription: Dict) -> Dict:
        """Handle subscription cancellation"""
        customer_id = subscription.get('customer')

        print(f"❌ Subscription cancelled: {customer_id}")

        return {
            'success': True,
            'action': 'deactivate_subscription',
            'customer_id': customer_id
        }

    def _handle_payment_failed(self, invoice: Dict) -> Dict:
        """Handle failed payment"""
        customer_id = invoice.get('customer')
        customer_email = invoice.get('customer_email')

        print(f"⚠️ Payment failed: {customer_email}")

        # TODO: Send email reminder

        return {
            'success': True,
            'action': 'payment_failed',
            'customer_id': customer_id,
            'customer_email': customer_email
        }

    def create_referral_coupon(self, referrer_id: str) -> Dict:
        """
        Create a 20% off coupon for referrals

        Args:
            referrer_id: ID of user who made the referral

        Returns:
            Dict with coupon code
        """
        try:
            coupon = stripe.Coupon.create(
                percent_off=20,
                duration='once',
                name=f'Referral from {referrer_id}',
                metadata={'referrer_id': referrer_id}
            )

            return {
                'success': True,
                'coupon_code': coupon.id
            }

        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }


# Example usage and testing
if __name__ == "__main__":
    processor = SparkPaymentProcessor()

    # Test: Create checkout session
    print("🧪 Testing Stripe integration...")
    result = processor.create_checkout_session(
        customer_email="test@example.com",
        tier="pro"
    )

    if result['success']:
        print(f"✅ Checkout URL: {result['checkout_url']}")
    else:
        print(f"❌ Error: {result['error']}")
