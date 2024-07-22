import os
import json
import requests

# Determine the authorization token
authorization = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE3MDk1LCJpc3MiOiJodHRwczovL2xvZ2luLmNybS5hY3NvbHV0aW9ucy5haS9hcGkvdj'

# Determine the BOT ID
botID = '37331'

# Define headers and parameters for the request
headers = {
    'accept': 'application/json, text/plain, */*',
    'authorization': authorization,
}

# Folder for saving files
download_folder = r'Нарпиндер_Провинциальный_Хинди'


# Check if the folder exists; if not, create it
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Execute the request
url1 = 'https://back.crm.acsolutions.ai/api/v2/bot/script/' + botID + '?'
response = requests.get(url1, headers=headers)

if response.status_code == 200:
    decoded_response = json.loads(response.text)
    screen = decoded_response['screens']
else:
    print("Ошибка при выполнении первого запроса:", response.status_code)
    decoded_response = []

for i in screen:
    for j in i['accosts']:
        for k in j['file']['list']:
            download_url = 'https://back.crm.acsolutions.ai/storage' + k
            file_name = k.split('/bot/accosts/')[1]
            file_path = os.path.join(download_folder, file_name)

            response = requests.get(download_url)

            if response.status_code == 200:
                # Save the file
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'Файл {file_name} успешно скачан в {download_folder}.')
            else:
                print(f'Не удалось скачать файл {file_name}. Статус-код: {response.status_code}')
