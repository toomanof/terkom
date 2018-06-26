import logging
from datetime import date, datetime
from ..models.reg_price import RegPrice
from ..models.registration import Registration


def post(invoce):
    Registration.objects.filter(invoce_id=invoce.id).delete()
    #RegPrice.objects.filter(invoce_id=invoce.id).delete()

    for item in invoce.items.all():
        summa = round(float(item.qty) * float(item.price), 2)
        registr = Registration(invoce=invoce, from_of=invoce.contractor,
                               product=item.product, qty=item.qty,
                               summa=summa, motion=invoce.motion,
                               created_at=invoce.created_at)
        registr.save()      
        
        if RegPrice.objects.filter(product=item.product)\
                   .filter(created_at=invoce.created_at).exists():
          reg_price = RegPrice(created_at=invoce.created_at,
                               product=item.product, price=item.price,
                               invoce=invoce)
          reg_price.save()
        else:                   
          RegPrice.objects.filter(product=item.product)\
                   .filter(created_at=invoce.created_at)\
                   .update(price=item.price, invoce=invoce)
        

def get_current_price(product, find_date=None):
    logging.error(product)
    if find_date is None:
        find_date = date(datetime.today())
    result = RegPrice.objects.filter(product_id=product.id).\
                              filter(created_at__lte=find_date).\
                              order_by('-created_at')
    return result[0].price if result else 0

def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict'''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
