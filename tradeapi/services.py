from django.shortcuts import get_object_or_404

from .models import Offer, Inventory, Wallet, Trade


def trade(buyer_offer, seller_offer):
    seller = seller_offer.user
    item = seller_offer.item
    buyer = buyer_offer.user

    Trade.objects.create(
        item=seller_offer.item,
        seller=seller,
        buyer=buyer,
        quantity=buyer_offer.entry_quantity,
        unit_price=buyer_offer.price,
        description="Trade",
        buyer_offer=buyer_offer,
        seller_offer=seller_offer
    )

    buyer_inventory = get_object_or_404(Inventory, user=buyer, item=item)

    seller_wallet = get_object_or_404(Wallet, user=seller)

    seller_wallet.money += seller_offer.price
    buyer_inventory.quantity += buyer_offer.entry_quantity

    buyer_offer.is_active = False

    if seller_offer.entry_quantity == 0:
        seller_offer.is_active = False

    seller_wallet.save()
    buyer_inventory.save()