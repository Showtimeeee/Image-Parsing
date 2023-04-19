import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_image(url):
    soup = bs(requests.get(url).content, 'html.parser')
    urls = []
    for img in tqdm(soup.find_all('img'), 'Скачивается'):
        img_url = img.attrs.get('src')
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index('?')
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)

    return urls


# сохраняем в папку, если ее нет то создаем
def download_img(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)

    file_size = int(response.headers.get('Content-Length', 0))

    file_name = os.path.join(pathname, url.split('/')[-1])

    progress_bar = tqdm(response.iter_content(1024), f'Загрузка {file_name}',
                    total=file_size, unit='B', unit_scale=True, unit_divisor=1024)

    with open(file_name, 'wb') as f:
        for data in progress_bar.iterable:
            f.write(data)
            progress_bar.update(len(data))


def main(url, path):
    imgs = get_image(url)
    for img in imgs:
        download_img(img, path)


if __name__ == '__main__':
    main('https://trends.rbc.ru/trends/industry/631b12769a79478aa69b6bf8', f'{os.getcwd()}/images')