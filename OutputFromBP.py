import json
import requests
import pandas as pd

# Defining an Authorization Token
authorization = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE3MDk1LCJpc3MiOiJodHRwczovL2xvZ2luLmNybS5hY3NvbHV0aW9ucy5haS9hcGkvdj'

# Defining an unique key BP
key = 'd5a4eb6636'

# Defining a date_from
date_from = '2024-06-19'

# Defining a date_to
date_to = '2024-06-24'


# Defining the headers and parametrs for the 1st and 2nd requests
headers1 = {
    'accept': 'application/json, text/plain, */*',
    'authorization': authorization,
}

params1 = {
    'key': key,
    'from': date_from,
    'to': date_to
}


# Excecuding the 1st request
url1 = 'https://back.crm.acsolutions.ai/api/v2/bpm/bp/' + key
response1 = requests.get(url1, params=params1, headers=headers1)
if response1.status_code == 200:
    decoded_response1 = json.loads(response1.text)
    actions1 = decoded_response1.get("actions", [])
else:
    print("Ошибка при выполнении первого запроса:", response1.status_code)
    actions1 = []


# Excecuding the 2nd request
url2 = 'https://back.crm.acsolutions.ai/api/v2/bpm/bp/get_stats/' + key
response2 = requests.get(url2, params=params1, headers=headers1)
if response2.status_code == 200:
    decoded_response2 = json.loads(response2.text)
    data2 = decoded_response2.get("data", {})
else:
    print("Ошибка при выполнении второго запроса:", response2.status_code)
    data2 = {}


# Creating a dictionary for storing statuses
action_statuses = {}

# Creating a dictionary to store the mapping of ID and title
id_to_title = {action.get("id"): action.get("title") for action in actions1}

# Iterating through the actions from the first response
for action1 in actions1:
    action_id = action1.get("id")

    # Searching for the corresponding status in the second response
    action_status = data2.get(str(action_id), {})

    # Retrieve the necessary statuses
    count = action_status.get("waiting", 0) + action_status.get("running", 0) + action_status.get("stuck", 0) + action_status.get("ended", 0) + action_status.get("was_transferred", 0)
    uncount = action_status.get("waiting", 0) + action_status.get("running", 0) + action_status.get("stuck", 0) + action_status.get("was_transferred", 0)
    # Get the title by ID
    title = id_to_title.get(action_id)
    # Save statuses in a dictionary
    if title in action_statuses:
        action_statuses[title]['count'] += count
        action_statuses[title]['uncount'] += uncount
    else:
        action_statuses[title] = {
            'action_id' : action_id,
            'count' : count,
            'uncount' : uncount,
        }



# Create a dictionary for final statuses
default = {'Автоответчик' : 0, 'Сброс' : 0, 'Другая фраза' : 0, 'Недозвон' : 0, 'Заинтересован' : 0, 'Не обработано' : 0,
           'Перезвон' : 0, 'Средне-заинтересованные' : 0, 'Formal Bot 1' : 0, 'Formal Bot 2' : 0, 'Formal Bot 3' : 0,
           'Автоответчик Д' : 0, 'Сброс Д' : 0, 'Другая фраза Д' : 0, 'Недозвон Д' : 0, 'Заинтересован СМС 1 Д' : 0,
           'Skittish Bot 1' : 0, 'Skittish Bot 2' : 0, 'Skittish Bot 3' : 0,
           'Автоответчик К' : 0, 'Сброс К' : 0, 'Другая фраза К' : 0, 'Недозвон К' : 0, 'Заинтересован СМС 1 К' : 0,
           'Hillybilly Bot 1' : 0, 'Hillybilly Bot 2' : 0, 'Hillybilly Bot 3' : 0,
           'Автоответчик П' : 0, 'Сброс П' : 0, 'Другая фраза П' : 0, 'Недозвон П' : 0, 'Заинтересован СМС 1 П' : 0,
           'Formal Bot EN 1' : 0, 'Formal Bot EN 2' : 0, 'Formal Bot EN 3' : 0,
           'Автоответчик EN' : 0, 'Сброс EN' : 0, 'Другая фраза EN' : 0, 'Недозвон EN' : 0, 'Заинтересован СМС EN 1' : 0}

# Filter data to populate the dictionary for final statuses
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

# Convert data into a DataFrame
df = pd.DataFrame.from_dict(default, orient='index')

# Save the DataFrame to an Excel file
excel_file_path = "dataBP.xlsx"
df.to_excel(excel_file_path)

print(f"Данные успешно записаны в Excel файл: {excel_file_path}")
