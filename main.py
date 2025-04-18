import os
import json
import requests
import time

api_endpoint = "http://localhost:41184"


def create_note_from_json(token: str, data: dict, notedpad_id: str):
    joplin_data = {
        'parent_id': notedpad_id,
        'title': generate_headline(data.get('textContent')) if data.get('title') == '' else data.get('title'),
        'body_html': data.get('textContentHtml', ''),
        'user_created_time': data.get('createdTimestampUsec') / 1000,
        'user_updated_time': data.get('userEditedTimestampUsec') / 1000
    }

    response = requests.post(f"{api_endpoint}/notes?token={token}", json=joplin_data)

    return response.json()


def create_new_notepad(token: str, name: str):
    if name == '':
        name = 'Google Keep'
        
    notepad_data = {
        'title': name
    }

    try:
        response = requests.post(f"{api_endpoint}/folders?token={token}", json=notepad_data)
        return response.json()['id']
    except:
        raise ValueError("Ошибка. Не удалось обработать токен авторизации")




def generate_headline(text_content: str):
    if len(text_content) > 23:
        if ' ' in text_content[23:]:
            text = text_content[:text_content.index(' ', 23)] + '...'
        else:
            text = text_content[:23] + '...'
    else:
        text = text_content


    return text


def main():
    directory = "Takeout/Google Keep/"

    json_files = []

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Небольшой скрипт для переноса текстовых заметок из Google Keep в Joplin")
    time.sleep(1)
    print("Необходимо зайти в параметры Joplin и найти 'Настройка веб-клиппера - > Включить службу веб-клиппера'")
    print("Во время переноса оставляйте приложение включенным")
    time.sleep(1)
    print("Введите токен авторизации, указанный в меню веб-клиппера: ")
    token = input()
    print('Введите имя блокнота, в который будут перенесены заметки (default: Google Keep):')
    notedpad_id = create_new_notepad(token, input())

    
    try:
        print("Начинаем процесс переноса")
        time.sleep(2)
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)

                with open(file_path, 'r') as f:
                    data = json.load(f)

                    if data.get('textContent') != '' and type(data.get('textContent')) == str:
                        create_note_from_json(token, data, notedpad_id)
        print("Перенос окончен")

    except:
        print("Ошибка. Не найдена папка для импорта")
        print("Необходимо скачать архив с заметками по ссылке https://takeout.google.com")
        print("После распаковать его в директорию с проектом")


if __name__ == "__main__":
    main()