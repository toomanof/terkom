import logging
from django.db import connection
from datetime import date, datetime
from ..models.reg_price import RegPrice
from ..models.registration import Registration
from ..constants import ARRIVAL, EXPENSE



def posting(invoce):
    metka = invoce
    for item in invoce.items.all():
        summa = round(float(item.qty) * float(item.price), 2)
        if invoce.motion == EXPENSE:
            metka = get_metka_product_qt_0('product', item.product.id)

        qty = item.qty if invoce.motion == ARRIVAL else  item.qty * -1
        registr, created = Registration.objects.get_or_create(
            invoce=invoce,
            product=item.product,
            defaults = {
                        'metka':metka,
                        'from_of':invoce.contractor,
                        'dish':item.product.dish,
                        'qty':qty,
                        'summa':summa,
                        'motion':invoce.motion,
                        'created_at':invoce.created_at}
        )

        if created:
          registr.delete()
        registr.save()

        if invoce.motion == ARRIVAL:
            reg_price, created  = RegPrice.objects.get_or_create(
                created_at=invoce.created_at,
                product=item.product,
                dish=item.product.dish,
                price=item.price,
                invoce=invoce)
            if created:
              reg_price.delete()
            reg_price.save()

def get_metka_product_qt_0(type_object, product):
    sql ='SELECT SUM(qty), metka_id\
          FROM calculation_registration\
          WHERE {}_id =%s\
          GROUP BY metka_id\
          ORDER BY created_at'.format(type_object)
    cursor = connection.cursor()
    cursor.execute(sql, [product])
    rows = cursor.fetchall()

    for row in rows:
        if row[0]>0:
            return row[1]
    return None

def get_first_product_price(object_id, type_object, find_date=None):
    invoice_id = get_metka_product_qt_0(type_object, object_id)
    if invoice_id:
        if find_date is None:
            find_date = date(datetime.today())
        sql = 'SELECT crp.price\
               FROM calculation_registration cr\
               LEFT JOIN calculation_regprice crp\
               ON cr.product_id = crp.product_id\
               AND cr.invoce_id = crp.invoce_id\
               WHERE crp.{}_id =%s AND cr.invoce_id={}\
               AND cr.created_at <= %s\
               ORDER BY cr.created_at LIMIT 1'.format(type_object, invoice_id)
        cursor = connection.cursor()
        cursor.execute(sql, [object_id,find_date])
        row = cursor.fetchone()
        return row[0] if row else 0
    else:
        return 0

def delete(invoce):
    Registration.objects.filter(invoce_id=invoce.id).delete()
    RegPrice.objects.filter(invoce_id=invoce.id).delete()


def get_current_price(dish_id, find_date=None):
    return get_first_product_price(dish_id,'dish', find_date)

def get_current_price_product(product_id, find_date=None):
    return get_first_product_price(dish_id,'product', find_date)

def dictfetchall(cursor):
    '''Returns all rows from a cursor as a dict'''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
