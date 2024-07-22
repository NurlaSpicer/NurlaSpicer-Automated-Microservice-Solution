import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def get_folder_id(drive_service, folder_url):
    # Разбираем URL папки, чтобы получить ID
    folder_id = folder_url.split('/')[-1]
    return folder_id

def upload_file_to_drive(file_path, folder_url):
    # Здесь необходимо указать путь к вашему JSON-файлу с учетными данными службы
    SERVICE_ACCOUNT_FILE = 'data-acs-60fe914f25ef.json'
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=credentials)

    # Получаем ID папки из URL
    folder_id = get_folder_id(drive_service, folder_url)

    if not folder_id:
        print('Ошибка: Не удалось получить ID папки из URL.')
        return None

    # Создаем метаданные файла для загрузки
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]  # ID папки, в которую хотите загрузить файл
    }

    # Создаем объект MediaFileUpload для загрузки файла
    media = MediaFileUpload(file_path, resumable=True)

    # Загружаем файл на Google Drive
    try:
        file = drive_service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        file_id = file.get('id')
        print('Файл успешно загружен. ID файла:', file_id)
        return file_id
    except Exception as e:
        print('Ошибка загрузки файла в Google Drive:', e)
        return None

# Пример использования функции
if __name__ == "__main__":
    excel_file_path = 'dataBP.xlsx'
    folder_url = 'https://drive.google.com/drive/folders/19XBd5UaEz5QCR_NoLWnMpTl2ImQSkXUI'
    file_id = upload_file_to_drive(excel_file_path, folder_url)