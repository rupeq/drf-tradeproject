from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers


from .models import *
from .enum import OrderTypeEnum

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_obj = User(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'code', 'name')


class ItemSerializer(serializers.ModelSerializer):

    currency = CurrencySerializer()

    class Meta:
        model = Item
        fields = ('code', 'name', 'currency', 'details', 'price')


class FavoriteListSerializer(serializers.ModelSerializer):

    item = ItemSerializer()

    class Meta:
        model = WatchList
        fields = ('item', 'user')
        extra_kwargs = {'user': {'read_only': True}}


class FavoriteCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = ('item', 'user')
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        user = self.context["request"].user
        watchlist = WatchList(user=user, **validated_data)
        watchlist.save()

        return watchlist


class OfferListSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    user = ListUserSerializer()

    class Meta:
        model = Offer
        fields = '__all__'


class OfferCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('item', 'entry_quantity', 'order_type', 'price')

    def create(self, validated_data):

        user = self.context["request"].user
        item = validated_data.get("item")
        inventory = get_object_or_404(Inventory, user=user, item=item)
        wallet = get_object_or_404(Wallet, user=user)

        order_type = validated_data.get('order_type')
        entry_quantity = validated_data.get('entry_quantity')
        price = validated_data.get('price')

        if order_type == OrderTypeEnum.OP_SELL.value:
            if inventory.quantity < entry_quantity:
                raise serializers.ValidationError("Inventory quantity less than entry quantity")
            inventory.quantity -= entry_quantity
        elif order_type == OrderTypeEnum.OP_BUY.value:
            if price * entry_quantity > wallet.money:
                raise serializers.ValidationError("Price great than wallet money")
            wallet.money -= price

        validated_data['quantity'] = inventory.quantity
        validated_data['user'] = user

        offer = Offer(**validated_data)
        offer.save()
        inventory.save()
        wallet.save()

        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('item', 'quantity', 'entry_quantity', 'order_type', 'transaction_type', 'price')


class InventoryListSerializer(serializers.ModelSerializer):

    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = "__all__"


class TradeSerializer(serializers.ModelSerializer):

    item = ItemSerializer()
    buy = UserSerializer()
    sell = UserSerializer()
    buy_offer = OfferListSerializer()
    sell_offer = OfferListSerializer()

    class Meta:
        model = Trade
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = "__all__"
