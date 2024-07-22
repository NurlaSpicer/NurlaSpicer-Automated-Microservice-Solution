import json
import requests
import pandas as pd

# Определяем authorization token
authorization = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE3MDk1LCJpc3MiOiJodHRwczovL2xvZ2luLmNybS5hY3NvbHV0aW9ucy5haS9hcGkvdjIvdXNlcnMvYXV0aCIsImlhdCI6MTcxOTIwOTIxMywiZXhwIjoxNzUwNzQ1MjEzLCJuYmYiOjE3MTkyMDkyMTMsImp0aSI6Inl1eEg4WHAxTkJRUVp0dlQifQ.C7K0-bjlNhJqrFDQVoipCAR0CoRksbIhlTJrQRUSfnc'

# Определяем key BP
key = 'd5a4eb6636'

# Определяем date_from
date_from = '2024-06-19'

# Определяем date_to
date_to = '2024-06-24'


# Определяем заголовки и параметры для первого запроса
headers1 = {
    'accept': 'application/json, text/plain, */*',
    'authorization': authorization,
}

params1 = {
    'key': key,
    'from': date_from,
    'to': date_to
}


# Выполняем первый запрос
url1 = 'https://back.crm.acsolutions.ai/api/v2/bpm/bp/' + key
response1 = requests.get(url1, params=params1, headers=headers1)
if response1.status_code == 200:
    decoded_response1 = json.loads(response1.text)
    actions1 = decoded_response1.get("actions", [])
else:
    print("Ошибка при выполнении первого запроса:", response1.status_code)
    actions1 = []


# Выполняем второй запрос
url2 = 'https://back.crm.acsolutions.ai/api/v2/bpm/bp/get_stats/' + key
response2 = requests.get(url2, params=params1, headers=headers1)
if response2.status_code == 200:
    decoded_response2 = json.loads(response2.text)
    data2 = decoded_response2.get("data", {})
else:
    print("Ошибка при выполнении второго запроса:", response2.status_code)
    data2 = {}


# Создаем словарь для хранения статусов
action_statuses = {}

# Создаем словарь для хранения соответствия id и title
id_to_title = {action.get("id"): action.get("title") for action in actions1}

# Проходимся по действиям из первого ответа
for action1 in actions1:
    action_id = action1.get("id")

    # Ищем соответствующий статус во втором ответе
    action_status = data2.get(str(action_id), {})

    # Получаем нужные статусы
    count = action_status.get("waiting", 0) + action_status.get("running", 0) + action_status.get("stuck", 0) + action_status.get("ended", 0) + action_status.get("was_transferred", 0)
    uncount = action_status.get("waiting", 0) + action_status.get("running", 0) + action_status.get("stuck", 0) + action_status.get("was_transferred", 0)
    # Получаем title по id
    title = id_to_title.get(action_id)
    # Сохраняем статусы в словаре
    if title in action_statuses:
        action_statuses[title]['count'] += count
        action_statuses[title]['uncount'] += uncount
    else:
        action_statuses[title] = {
            'action_id' : action_id,
            'count' : count,
            'uncount' : uncount,
        }



# Создаем dictionary для конечных статусов
default = {'Автоответчик' : 0, 'Сброс' : 0, 'Другая фраза' : 0, 'Недозвон' : 0, 'Заинтересован' : 0, 'Не обработано' : 0,
           'Перезвон' : 0, 'Средне-заинтересованные' : 0, 'Formal Bot 1' : 0, 'Formal Bot 2' : 0, 'Formal Bot 3' : 0,
           'Автоответчик Д' : 0, 'Сброс Д' : 0, 'Другая фраза Д' : 0, 'Недозвон Д' : 0, 'Заинтересован СМС 1 Д' : 0,
           'Skittish Bot 1' : 0, 'Skittish Bot 2' : 0, 'Skittish Bot 3' : 0,
           'Автоответчик К' : 0, 'Сброс К' : 0, 'Другая фраза К' : 0, 'Недозвон К' : 0, 'Заинтересован СМС 1 К' : 0,
           'Hillybilly Bot 1' : 0, 'Hillybilly Bot 2' : 0, 'Hillybilly Bot 3' : 0,
           'Автоответчик П' : 0, 'Сброс П' : 0, 'Другая фраза П' : 0, 'Недозвон П' : 0, 'Заинтересован СМС 1 П' : 0,
           'Formal Bot EN 1' : 0, 'Formal Bot EN 2' : 0, 'Formal Bot EN 3' : 0,
           'Автоответчик EN' : 0, 'Сброс EN' : 0, 'Другая фраза EN' : 0, 'Недозвон EN' : 0, 'Заинтересован СМС EN 1' : 0}

# Фильтруем данные для заполнения dictionary для конечных статусов
for i in default:
    try:
        if i != 'Автоответчик' and i != 'Сброс' and i != 'Другая фраза' and i != 'Недозвон' and i != 'Заинтересован':

            if i.__contains__('Formal Bot 2') or i.__contains__('Skittish Bot 2') or i.__contains__('Hillybilly Bot 2') or i.__contains__('Formal Bot EN 2'):
                default['Перезвон'] += action_statuses[i]['count']

            if i.__contains__('Автоответчик'):
                default['Автоответчик'] += action_statuses[i]['count']

            elif i.__contains__('Сброс'):
                default['Сброс'] += action_statuses[i]['count']

            elif i.__contains__('Другая фраза'):
                default['Другая фраза'] += action_statuses[i]['count']

            elif i.__contains__('Недозвон'):
                default['Недозвон'] += action_statuses[i]['count']

            elif i.__contains__('Заинтересован'):
                default['Заинтересован'] += action_statuses[i]['count']

            elif (i.__contains__('Не обработано') or i.__contains__('Formal Bot 1') or i.__contains__('Formal Bot 2')
                  or i.__contains__('Formal Bot 3') or i.__contains__('Skittish Bot 1') or i.__contains__('Skittish Bot 2')
                  or i.__contains__('Skittish Bot 3') or i.__contains__('Hillybilly Bot 1') or i.__contains__('Hillybilly Bot 2')
                  or i.__contains__('Hillybilly Bot 3') or i.__contains__('Formal Bot EN 1') or i.__contains__('Formal Bot EN 2')
                  or i.__contains__('Formal Bot EN 3')):
                default['Не обработано'] += action_statuses[i]['uncount']

            elif i.__contains__('Средне-заинтересованные'):
                for j in action_statuses:
                    if j.__contains__('Средне-заинтересованные'):
                        default[i] += action_statuses[j]['count']

            default[i] = action_statuses[i]['count']
    except KeyError:
        print('Key not found: ', i)

print(default)

# Преобразуем данные в DataFrame
df = pd.DataFrame.from_dict(default, orient='index')

# Сохраняем DataFrame в Excel файл
excel_file_path = "dataBP.xlsx"
df.to_excel(excel_file_path)

print(f"Данные успешно записаны в Excel файл: {excel_file_path}")