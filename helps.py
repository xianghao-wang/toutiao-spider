import os
import requests
from urllib.parse import urlencode
from hashlib import md5

def get_one_page(offset):
    params = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': os.getenv('KEYWORD'),
        'autoload': 'true',
        'count': 20
    }

    url = os.getenv('BASE_URL') + '?' + urlencode(params)
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images:
                for image in images:
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }

def save_image(item):
    dir_path = '{0}/{1}'.format(os.getenv('IMG_DIR'), item.get('title'))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        resp = requests.get(item.get('image'))
        if resp.status_code == 200:
            file_path = '{0}/{1}/{2}.{3}'.format(os.getenv('IMG_DIR'), item.get('title'), md5(resp.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
    except requests.ConnectionError:
        print('Filed to save image')