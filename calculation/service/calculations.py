import logging

from django.db.models import Max

from ..models import Menu, MenuItems, Registration, Product
from ..models import Dish, MapItems, Map, Invoice, InvoiceItems
from .helpers import get_current_price
from ..constants import *




def get_report_calculation_of_day(day, qty_children):
    '''
        Функция выбирает меню на день: day.
        Формирует матрицу блюд по оси Y и ингридиенты с весом
        на одно блюдо и весом на все блюда по оси X
        Возращает Матрицу меню и список продуктов задействованных
        в меню.
    '''
    keys_col_table = ('product', 'netto_all', 'netto_one','product_id')
    keys_ingr = ('product_id', 'product__name',
                 'product__tech_map', 'brutto',)
    products = []  # Список всех ингридиентов в меню дня
    table_calculation = []  # Основная таблица
    row_table = {'dish': None, 'cols': []}  # Структура строки
    # Структура колонки
    # col_table = {'product': None, 'netto_all': 0, 'netto_one': 0}


    def append_table(**vars):
        if 'dish' in vars:
            new_row =row_table.copy()
            new_row['dish'] = vars['dish']
        if 'row' in vars:
            new_row = vars['row']
        table_calculation.append(new_row)

    def sort_ingredients(A,field_sort=None):
        alen = len(A)
        for index in range(1, alen):
            for k in range(0, alen - index):
                chahge =A[k][field_sort] > A[k + 1][field_sort]\
                    if field_sort is not None else  A[k] > A[k + 1]
                if chahge:
                    A[k], A[k + 1] = A[k + 1], A[k]                  
        return A

    def get_ingredients(tech_map_id, result=[]):
        '''
            Функция выбирает все ингридиенты входящие в переданую
            тех. карту, а также все ингридиенты по исходящей в глубь 
        '''
        # Выбираем ингридиенты входящие в тех карту
        ingredients = list(
                MapItems.objects
                    .filter(map_doc_id=tech_map_id)
                    .select_related('product')
                    .values(*keys_ingr)
                    .order_by('product__name'))
        # Из них выбираем ингридиенты которые сами имеют ингридиенты
        products_with_ingr =list(
            filter(lambda item: item['product__tech_map'] is not None,
                   ingredients))

        # Для каждого выбраного ингридиента выбираем его ингридиенты
        # и добавляем в общий список ингридиентов первоначальной тех карты
        for product in products_with_ingr:
            result = get_ingredients(product['product__tech_map'], result)
        
        result += list(filter(lambda item: item['product__tech_map'] is None,
                       ingredients))
        return result

    # Выбираются из базы id меню за день
    menu_list = list(Menu.objects.filter(created_at=day)
                                 .values('id', 'food_intake'))
    menu_list_with = []
    for menu in menu_list:
        # Создем словарь приема пищи со списком блюд
        food_intake_menu = {'food_intake_name':
                            TYPE_FOOD_INTAKE[int(menu['food_intake']) - 1][1],
                            'food_intake_id': int(menu['food_intake'])}

        # Выбираются из базы список используемых блюд за день
        dishs_in_menu = list(
            MenuItems.objects.filter(invoce_doc_id=menu['id'])
                             .select_related('dish')
                             .values('id', 'out', 'dish_id',
                                     'dish__name', 'dish__tech_map',
                                     'dish__tech_map__batch_output')
                             .order_by('dish__name'))
        print('dishs',dishs_in_menu)
        for dish_in_menu in dishs_in_menu:
            # Запоминаем значение выхода веса по тех. карте
            # Изменяем ключ на map_out 
            dish_in_menu['map_out'] =\
            dish_in_menu.pop('dish__tech_map__batch_output')
            # Изменяем тип значение на целое число
            dish_in_menu['map_out'] =\
                int(dish_in_menu['map_out'].split(',')[0])\
                    if dish_in_menu['map_out'] is not None else 0
            # Запоминаем значение выхода веса указываем 
            # то, что указано в меню
            dish_in_menu['out'] =\
                int(dish_in_menu['out'].split(',')[0])\
                    if dish_in_menu['out'] is not None else 0
            # Вычисляем входящие ингридиенты в блюдо
            if dish_in_menu['dish__tech_map'] is not None:
                dish_in_menu['ingredients'] =sort_ingredients(
                    get_ingredients(dish_in_menu['dish__tech_map'],[]),
                    'product__name')
            else: # если не указана тех. карта, тогда блюдо само ингридиент
                if 'ingredients' not in dish_in_menu:
                    dish_in_menu['ingredients'] = []
                # заносим продукт в ингридиенты самого продукта  
                dish_in_menu['ingredients'].append(
                    dict(zip(keys_ingr,
                             [dish_in_menu['dish_id'],
                              dish_in_menu['dish__name'],
                              None,dish_in_menu['out']])))
            
            #print('dish', dish_in_menu)
            for item in dish_in_menu['ingredients']:
                for product in products:
                    if product['name'] == item['product__name']:
                        break
                else:
                    products.append({'name': item['product__name'],
                                     'id': item['product_id']})
            sort_ingredients(products,'name') 
            print('products',)
            print(products)
        food_intake_menu['dishs'] = dishs_in_menu
        menu_list_with.append(food_intake_menu)
    # Собрали сведения для расчета теперь давай расчитвать
    # и подставлять в результирующую таблицу
    count_ingridients = len(products)
    total_weigth = {product['name']: 0 for product in products}
    for food_intake_menu in menu_list_with:
        append_table(dish=food_intake_menu['food_intake_name'])
        for dish in food_intake_menu['dishs']:
            coefficient =1;
            if dish['map_out'] > 0: 
                coefficient = int(dish['out']) / int(dish['map_out'])

            row_dish ={'dish': dish['dish__name'],
                       'id_row':dish['id'],
                       'cols': []}
            for product in products:
                for ingredient in dish['ingredients']:
                    if product['name'] == ingredient['product__name']:
                       
                        weigth_all = float(ingredient['brutto']) *\
                             coefficient / 1000 * float(qty_children)
                        row_dish['cols'].append(
                            dict(zip(
                                keys_col_table,
                                [product['name'], weigth_all,
                                 float(ingredient['brutto']) * coefficient])))
                        
                        total_weigth[product['name']] += weigth_all
                        break
                else:
                    row_dish['cols'].append(
                        dict(zip(keys_col_table,[product['name'], 0, 0])))
            append_table(row=row_dish)
   
    # Приводятся к типу матрицы итоговые значения
    row_weight = {'dish': 'Всего, кг:','id_row':'weight'}
    row_weight['cols'] = \
        [dict(zip(keys_col_table, (product['name'], 
                                   total_weigth[product['name']], 0, 
                                   product['id'])))
         for product in products]
    append_table(row=row_weight)
    # Приводятся к типу матрицы цены продуктов действующие
    # на день калкуляции    
    row_price = {'dish': 'Цена, руб:', 'id_row':'price'}
    row_price['cols'] = [dict(zip(keys_col_table,
                                         (product['name'],
                                          get_current_price(int(product['id']), day))))
                                for product in products]
    append_table(row =row_price)

    row_total = {'dish': 'Сумма, руб:', 'id_row':'total'}
    row_total['cols'] = []
    all_total = 0
    price_ingr = row_price['cols']
    weight_ingr = row_weight['cols']
    for index in range(0, len(price_ingr)):
        d = {keys_col_table[0]: price_ingr[index][keys_col_table[0]],
             keys_col_table[1]: round(float(price_ingr[index][keys_col_table[1]]) *
                                float(weight_ingr[index][keys_col_table[1]]), 2)}

        row_total['cols'].append(d)
        all_total += d[keys_col_table[1]]
    append_table(row=row_total)

    return {'calculation_day': table_calculation, 'products': products,
            'all_total': all_total,
            'total_per_child': all_total / qty_children,
            'count_ingridients': (count_ingridients - 1) * 2 +3}


def get_report_product_accounting(period):
    '''
        Функция возращает отчет по движению товара на складе
        за период: period.
    '''
    table = []
    products_in_period = Registration.objects.\
        filter(created_at__gte=period['from']).\
        filter(created_at__lte=period['to']).\
        values_list('product', flat=True).distinct()
    for product in products_in_period:
        row_product = {}
        row_product['product'] = Product.objects.get(pk=product)
        registrs_period = Registration.objects.\
            filter(product=product).\
            filter(created_at__gte=period['from']).\
            filter(created_at__lte=period['to']).\
            order_by('invoce__motion')
        row_product['invoices'] = registrs_period
        table.append(row_product)
    return {'report_product_accounting': table}


def get_invoice_out(day, qty_children):
    max_id = InvoiceItems.objects.aggregate(Max('id'))['id__max']
    max_id_invoice = Invoice.objects.aggregate(Max('id'))['id__max']

    data_calc = get_report_calculation_of_day(day, qty_children)
    # Выбираем две строки: 'weight', 'price'
    if data_calc:
        stop  = 0
        data ={}
        for row in data_calc['calculation_day']:
            if 'id_row' in row:
                if row['id_row'] in ('weight', 'price'):
                    data[row['id_row']] = row['cols']
                    stop += 1
            if stop == 2:
                break
        for item in data['price']:
            item['price'] = item.pop('netto_all')

        # Объединяем словари двух строк: 'weight', 'price'
        new_data =[{**data['weight'][x], **data['price'][x]} 
                   for x in xrange(0,len(data['weight']))]

        # Создается список с новыми id InvoiceItems
        new_invoice_items_id = list(range(max_id + 1, 
                                          max_id + len(new_data) + 1))        
        # Объединяем данные с репорта с новыми id-шниками
        products =list(zip(new_data, new_invoice_items_id))
        for item in products:
            product = Product.objects.filter(name=item[0]['product'])
            if not product.exists():
                products.remove(item)
            else:
                item[0]['product_id'] = product[0].pk

        new_invoice = Invoice(number='{} {}'.format(max_id_invoice+1 ,day),
                              created_at=day,
                              motion=EXPENSE) 
        new_invoice.save()

        new_invoice_items = [InvoiceItems(
            id=item[1],
            invoce_doc_id=new_invoice.id,
            position =item[1]-max_id,
            product_id=item[0]['product_id'],
            qty=round(item[0]['netto_all']),
            price=float(item[0]['price'])) for item in products]
        InvoiceItems.objects.bulk_create(new_invoice_items)
    return