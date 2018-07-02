import logging
from datetime import date, datetime
from ..models.reg_price import RegPrice
from ..models.registration import Registration


def post(invoce):

    #Registration.objects.filter(invoce_id=invoce.id).delete()
    #RegPrice.objects.filter(invoce_id=invoce.id).delete()

    for item in invoce.items.all():
        summa = round(float(item.qty) * float(item.price), 2)
        registr = Registration.objects.filter(invoce=invoce,
                                              product=item.product,
                                              motion=invoce.motion)
        if not registr:
            registr = Registration(invoce=invoce,
                                   from_of=invoce.contractor,
                                   product=item.product,
                                   qty=item.qty,
                                   summa=summa, motion=invoce.motion,
                                   created_at=invoce.created_at)
            registr.save()
        else:
            registr.update(from_of=invoce.contractor,
                           created_at=invoce.created_at,
                           qty=item.qty, summa=summa)

        reg_price = RegPrice.objects.filter(product=item.product,
                                            invoce=invoce)
        if not reg_price:
            reg_price = RegPrice(created_at=invoce.created_at,
                                 product=item.product,
                                 dish=item.product.dish,
                                 price=item.price,
                                 invoce=invoce)
            reg_price.save()
        else:
            reg_price.update(dish=item.product.dish,
                             price=item.price,
                             created_at=invoce.created_at)


def delete(invoce):
    Registration.objects.filter(invoce_id=invoce.id).delete()
    RegPrice.objects.filter(invoce_id=invoce.id).delete()


def get_current_price(dish_id, find_date=None):
    if find_date is None:
        find_date = date(datetime.today())
    result = RegPrice.objects.filter(dish_id=dish_id,
                                     created_at__lte=find_date).\
                              order_by('-created_at')
    return result[0].price if result else 0

def get_current_price_product(product_id, find_date=None):
    if find_date is None:
        find_date = date(datetime.today())
    result = RegPrice.objects.filter(product_id=product_id,
                                     created_at__lte=find_date).\
                              order_by('-created_at')
    return result[0].price if result else 0

def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict'''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
