from django.urls import path
from .views import configure_cdp, create_wallet

urlpatterns = [
    path('configure_cdp/', configure_cdp, name='configure_cdp'),   
    path('create_wallet/', create_wallet, name='create_wallet'),
]

