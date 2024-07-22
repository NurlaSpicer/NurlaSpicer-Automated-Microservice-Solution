import os
import json
import requests

# Определяем authorization token
authorization = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE1NzIzLCJpc3MiOiJodHRwczovL2xvZ2luLmNybS5hY3NvbHV0aW9ucy5haS9hcGkvdjIvdXNlcnMvYXV0aCIsImlhdCI6MTcyMTIwMzg1MiwiZXhwIjoxNzUyNzM5ODUyLCJuYmYiOjE3MjEyMDM4NTIsImp0aSI6IkxXQlZEczNOZ3I5akh0VEUifQ.w1iGUHgQ6ZpHLLkT0e_JMPj3VHpkf1O5Ijjo1tHuTm8'

# Определяем key BP
botID = '37331'

# Определяем заголовки и параметры для первого запроса
headers = {
    'accept': 'application/json, text/plain, */*',
    'authorization': authorization,
}

# Папка для сохранения файлов
download_folder = r'Нарпиндер_Провинциальный_Хинди'


# Проверка, существует ли папка, если нет - создаем её
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Выполняем первый запрос
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
                # Сохранение файла
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'Файл {file_name} успешно скачан в {download_folder}.')
            else:
                print(f'Не удалось скачать файл {file_name}. Статус-код: {response.status_code}')