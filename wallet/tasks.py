import logging
from huey.contrib.djhuey import db_task
from .models import Wallet,WalletTransaction
from commerce.models import Cart
from functools import reduce

logger = logging.getLogger("huey")

@db_task
def handle_webhook(payload:dict) :
    logger.info("handling webhook event for {}".format(payload["event"]))
    if payload["event"] == "charge.success" :
        paystack_payment_ref = payload["data"]["reference"]
        try :
            wallet = WalletTransaction.objects.get(paystack_payment_ref=paystack_payment_ref)
            user = wallet.wallet.user
            carts = Cart.objects.filter(owner=user).filter(paid=False).values()
            acc_list = list(carts)
            acc_amount = reduce(lambda prev, curr: prev + curr["count"] * curr["price"], acc_list,0)
            amount = (payload["data"]["amount"]//100 )- 1500
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
            acc_amount = reduce(lambda prev, curr: prev + curr["count"] * curr["price"], acc_list,0)
            amount = payload["data"]["amount"]
            if acc_amount == amount :
                Cart.objects.filter(owner=user).filter(paid=False).update(paid=True)
        except :
            logger.error("can't find transaction with ID {}".format(paystack_payment_ref))
            
