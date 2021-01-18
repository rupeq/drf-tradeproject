from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .api_views import (ItemsView,
                        CurrencyView,
                        FavoriteList,
                        InventoryList,
                        OfferList,
                        TradeList,
                        WalletList)


router = DefaultRouter()
router.register(r'currency', CurrencyView, basename="currency")
router.register(r'items', ItemsView, basename="shares")
router.register(r'watchlist', FavoriteList, basename="favorite")
router.register(r'offers', OfferList, basename="offers")
router.register(r'inventory', InventoryList, basename='inventory')
router.register(r'trade', TradeList, basename='trade')
router.register(r'wallet', WalletList, basename='wallet')


urlpatterns = [
    path(r'', include(router.urls, )),
]
