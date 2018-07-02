import logging
from ..models import Menu, Registration, Product
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

    keys_row = ('product', 'netto_all', 'netto_one',)
    products = []

    def select_ingredients(dish_ingredients, ingredients):
        '''
            Выбор по рекурсии всех ингридиентов входящих
            в состав блюда
        '''

        if dish_ingredients:
            # если блюдо готовилось на основе технологической карты,
            # то выбираются задействованные продукты
            ingredients += [dict(zip(keys_row,
                                     [ingredient.product,
                                      ingredient.brutto / 1000 * qty_children,
                                      ingredient.brutto, 0]))
                            for ingredient in dish_ingredients]

            for ingredient in dish_ingredients:
                if hasattr(ingredient, 'ingredients'):
                    select_ingredients(ingredient.ingredients, ingredients)
        else:
            # если блюдо самостоятельный продукт, то в список ингридиентов
            # включается он сам
            out = item.out.split(',')
            ingredients.append(dict(zip(keys_row,
                                        [item.dish,
                                         int(out[0]) / 1000 * qty_children,
                                         int(out[0]), 0])))
            return

    def sort_ingredients(ingredients):
        alen = len(ingredients)
        for index in range(1, alen):
            for k in range(0, alen - index):
                if ingredients[k].name > ingredients[k+1].name:
                    ingredients[k], ingredients[k+1] = ingredients[k+1], ingredients[k]
        return

    calculation_day = []
    for menu in Menu.objects.filter(created_at=day):
        calculation_day.append({'food_intake': TYPE_FOOD_INTAKE[menu.food_intake-1][1]})
        for item in menu.rows:
            row_calc = {'dish': item.dish}
            ingredients = []
            # выбираюся блюда с продуктами присутвующими в них
            select_ingredients(item.dish.ingredients, ingredients)
            row_calc['ingredients'] = ingredients
            calculation_day.append(row_calc)

            # список всех продуктов действующие на день калкуляции
            products += tuple(ingredient[keys_row[0]] for ingredient in ingredients
                              if ingredient[keys_row[0]] not in products)
    sort_ingredients(products)
    count_ingridients = len(products)
    # создается пустой словарь сумм весов продуктов на всех детей
    total_weigth = {product: 0 for product in products}

    # создается матрица со всеми блюдами и всеми ингридиентами
    tabl = []    
    for item_dish in calculation_day:
        if 'food_intake' in item_dish:
            tabl.append(item_dish)
        else:
            row_calc = {'dish': item_dish['dish']}
            col_products = []
            for product in products:
                for dish_ingredient in item_dish['ingredients']:
                    if dish_ingredient[keys_row[0]] == product:
                        total_weigth[product] += float(
                            dish_ingredient[keys_row[1]])
                        col_products.append(dish_ingredient)
                        break
                else:
                    col_products.append(dict(zip(keys_row,
                                                 [product, 0, 0])))
                row_calc['ingredients'] = col_products
        tabl.append(row_calc)

    # Приводятся к типу матрицы итоговые значения
    row_weight = {'dish': 'Всего, кг:'}
    row_weight['ingredients'] = \
        [dict(zip(keys_row, (product, total_weigth[product])))
         for product in products]

    tabl.append(row_weight)

    # Приводятся к типу матрицы цены продуктов действующие
    # на день калкуляции
    row_price = {'dish': 'Цена, руб:'}
    row_price['ingredients'] = [dict(zip(keys_row,
                                         (product,
                                          get_current_price(product, day))))
                                for product in products]
    tabl.append(row_price)

    row_total = {'dish': 'Сумма, руб:'}
    row_total['ingredients'] = []
    all_total = 0
    price_ingr = row_price['ingredients']
    weight_ingr = row_weight['ingredients']
    for index in range(0, len(row_price['ingredients'])):
        d = {keys_row[0]: price_ingr[index][keys_row[0]],
             keys_row[1]: round(float(price_ingr[index][keys_row[1]]) *
                                float(weight_ingr[index][keys_row[1]]), 2)}

        row_total['ingredients'].append(d)
        all_total += d[keys_row[1]]
    tabl.append(row_total)

    return {'calculation_day': tabl, 'products': products,
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
    logging.error(table)
    return {'report_product_accounting': table}
