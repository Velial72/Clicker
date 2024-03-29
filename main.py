import argparse
import requests
import os
from dotenv import load_dotenv


def is_bitlink(token, link):
    headers = {"Authorization": f"Bearer {token}"}
    endpoint = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
    response = requests.get(endpoint, headers=headers)
    return response.ok


def shorten_link(token, link):
    api_url = 'https://api-ssl.bitly.com/v4/shorten'
    body = {"long_url": link}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api_url, headers=headers, json=body)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, link):
    headers = {"Authorization": f"Bearer {token}"}
    api_endpoint = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    response = requests.get(api_endpoint, headers=headers)
    response.raise_for_status()
    count = response.json()["total_clicks"]
    return count


def main():
    load_dotenv()
    token = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Программа позволяет сокращать ссылки и считать переходы по ним')
    parser.add_argument('link', help='Введи ссылку')
    args = parser.parse_args()

    try:
        link = args.link
        if is_bitlink(token, link):
            count = count_clicks(token, link)
            print(f"Количество кликов {count}")
        else:
            print(shorten_link(token, link))
    except requests.HTTPError:
        print("Введен некорректный адрес")


if __name__ == '__main__':
    main()
