from pathlib import Path
from urllib.parse import urljoin
import requests
from os import path
from pathvalidate import sanitize_filename


def download_image(img_url, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = urljoin('http://tululu.org', img_url)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    filename = img_url.split('/')[-1]
    filepath = path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_txt(response, title, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    if len(title) > 130:  # Чтобы ограничить кол-во символов в названии файла и предотвратить OSError.
        title = title[:130]
    filename = sanitize_filename(f'{title}.txt')
    filepath = path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath
