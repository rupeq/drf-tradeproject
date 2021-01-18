from celery import shared_task

from .services import trade
from .models import Offer
from .enum import OrderTypeEnum


@shared_task
def get_trade():
    buyer_offers = Offer.objects.select_related(
        'user',
        'item'
    ).filter(is_active=True, order_type=OrderTypeEnum.OP_BUY.value)

    for buyer_offer in buyer_offers:
        seller_offers = Offer.objects.select_related(
            'user',
            'item'
        ).filter(is_active=True,
                 order_type=OrderTypeEnum.OP_SELL.value,
                 price=buyer_offer.price,
                 item=buyer_offer.item).order_by("-price")

        if seller_offers.exists():
            trade(buyer_offer=buyer_offer, seller_offer=seller_offers[0])

