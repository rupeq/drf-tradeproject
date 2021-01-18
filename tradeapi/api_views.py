from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins

from tradeapi.models import Item, WatchList, Offer, Inventory, Trade, Currency, Wallet
from tradeapi.serializers import (ItemSerializer,
                                  CurrencySerializer,
                                  FavoriteListSerializer,
                                  FavoriteCreateSerializer,
                                  InventoryListSerializer,
                                  OfferCreateSerializer,
                                  OfferListSerializer,
                                  OfferUpdateSerializer,
                                  TradeSerializer,
                                  WalletSerializer)


class CurrencyView(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class ItemsView(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class FavoriteList(viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin,
                   viewsets.mixins.RetrieveModelMixin,
                   viewsets.mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    default_serializer_class = FavoriteListSerializer

    serializer_classes_by_action = {
        "list": FavoriteListSerializer,
        "create": FavoriteCreateSerializer,
        "update": FavoriteCreateSerializer,
        "retrieve": FavoriteListSerializer
    }

    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)


class InventoryList(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = InventoryListSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Inventory.objects.filter(user=user)


class OfferList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    default_serializer_class = OfferListSerializer

    permission_classes = (IsAuthenticated, )

    serializer_classes_by_action = {
        "list": OfferListSerializer,
        "create": OfferCreateSerializer,
        "update": OfferUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return Offer.objects.filter(is_active=True)


class TradeList(mixins.ListModelMixin,
                viewsets.GenericViewSet):

    serializer_class = TradeSerializer
    queryset = Trade.objects.all()

    permission_classes = (IsAuthenticated, )


class WalletList(mixins.ListModelMixin,
             viewsets.GenericViewSet):

    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
