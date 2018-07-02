ARRIVAL = 1
EXPENSE = 0
TITLE_MAIN_PAGE = 'Главная'

COPY_TO_TOMORROW = 'copytotomorrow'
COPY_TO_MONTH = 'copytomonth'

ACTIONS = ('Создание', 'Редактирование')

TYPE_CHOICES = ((ARRIVAL, 'приход'),
                (EXPENSE, 'расход'),)

TYPE_FOOD_INTAKE = ((1, 'Завтрак'),
                    (2, 'Обед'),
                    (3, 'Полдник'),
                    (4, 'ужин 1-й '),
                    (5, 'ужин 2-й'),)

TYPE_FOOD_INTAKE_ENG = ('breakfast',
                        'lunch',
                        'afternoon_snack',
                        'dinner_1',
                        'dinner_2')

INTERIOR = 'внутренний'
OUTER = 'внешний'
TYPE_CHOICES_CONTRACTOR = ((INTERIOR, 'внутренний'), (OUTER, 'внешний'),)
