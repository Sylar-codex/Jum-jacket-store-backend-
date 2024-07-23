import logging
from huey.contrib.djhuey import db_task
from .models import Wallet,WalletTransaction, WalletTransactionStripe
from commerce.models import Cart
from functools import reduce
import stripe

logger = logging.getLogger(__name__)


@db_task()
def handle_webhook(payload:dict) :
    logger.info("handling webhook event for {}".format(payload["event"]))
    if payload["event"] == "charge.success" :
        paystack_payment_ref = payload["data"]["reference"]
        try :
            wallet = WalletTransaction.objects.get(paystack_payment_ref=paystack_payment_ref)
            user = wallet.wallet.user
            carts = Cart.objects.filter(owner=user).filter(paid=False).values()
            acc_list = list(carts)
            acc_amount = reduce(lambda prev, curr: prev + curr["count"] * curr["price_naira"], acc_list,0)
            amount = (payload["data"]["amount"]//100 ) - 1500
            if acc_amount == amount :
                Cart.objects.filter(owner=user).filter(paid=False).update(paid=True)
        except :
            logger.error("can't find transaction with ID {}".format(paystack_payment_ref))
    elif payload["event"] == "transfer.success" :
        paystack_payment_ref = payload["reference"]
        try:
            wallet = WalletTransaction.objects.get(paystack_payment_ref=paystack_payment_ref)
            user = wallet.wallet.user
            carts = Cart.objects.filter(owner=user).filter(paid=False).values()
            acc_list = list(carts)
            acc_amount = reduce(lambda prev, curr: prev + curr["count"] * curr["price_naira"], acc_list,0)
            amount =( payload["data"]["amount"]//100) - 1500
            if acc_amount == amount :
                Cart.objects.filter(owner=user).filter(paid=False).update(paid=True)
        except :
            logger.error("can't find transaction with ID {}".format(paystack_payment_ref))


# handle webhook for stripe
@db_task()
def handle_stripe_webhook(payload:dict) :
    event = stripe.Event.construct_from(
      payload, stripe.api_key
    )
    logger.info("handling webhook event for {}".format(event))
    if event.type == 'payment_intent.succeeded' :
        payment_intent = event.data.object
        stripe_payment_intent = payment_intent["id"]
        try :
            wallet = WalletTransactionStripe.objects.get(stripe_payment_intent=stripe_payment_intent)
            user = wallet.wallet.user
            carts = Cart.objects.filter(owner=user).filter(paid=False).values()
            acc_list = list(carts)
            acc_amount = reduce(lambda prev, curr: prev + curr["count"] * curr["price_dollar"], acc_list,0)
            amount = (payment_intent["data"]["amount"]//100 ) - 20
            if acc_amount == amount :
                Cart.objects.filter(owner=user).filter(paid=False).update(paid=True)
        except :
            logger.error("can't find transaction with ID {}".format(stripe_payment_intent))
    elif payload["event"] == "transfer.success" :
        stripe_payment_intent = payload["reference"]
        try:
            wallet = WalletTransactionStripe.objects.get(stripe_payment_intent=stripe_payment_intent)
            user = wallet.wallet.user
            carts = Cart.objects.filter(owner=user).filter(paid=False).values()
            acc_list = list(carts)
            acc_amount = reduce(lambda prev, curr: prev + curr["count"] * curr["price_dollar"], acc_list,0)
            amount = (payment_intent["data"]["amount"]//100 ) - 20
            if acc_amount == amount :
                Cart.objects.filter(owner=user).filter(paid=False).update(paid=True)
        except :
            logger.error("can't find transaction with ID {}".format(stripe_payment_intent))
    print("stripe webhook")