from django.urls import include,path

from .api import DepositFundsAPI, WalletInfoAPI,VerifyDepositAPI,PaystackWebhookView,DepositInStripeAPI,StripeWebhookView

urlpatterns = [
    path('api/wallet_info', WalletInfoAPI.as_view()),
    path('api/deposit', DepositFundsAPI.as_view()),
    path('api/deposit/verify/<str:reference>/',VerifyDepositAPI.as_view()),
    path('api/paystack_webhook/',PaystackWebhookView.as_view()),
    path('api/deposit_stripe',DepositInStripeAPI.as_view()),
    path('api/stripe_webhook/',StripeWebhookView.as_view()),
]