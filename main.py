import argparse
import requests
import os
from dotenv import load_dotenv


def test_link(token, link):
  headers = {"authorization": token}
  url_test = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
  response = requests.get(url_test, headers=headers)
  result = response.ok
  return result


def shorten_links(token, link):
  url = 'https://api-ssl.bitly.com/v4/shorten'
  body = {"long_url":  link}
  headers = {"authorization": token}
  response = requests.post(url, headers=headers, json=body)
  response.raise_for_status()
  bitlink = response.json()['link']
  return bitlink


def count_clicks(token, link):
  headers = {"authorization": token}
  url_2 = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
  respons = requests.get(url_2, headers=headers)
  respons.raise_for_status()
  count = respons.json()["total_clicks"]
  return count

def main():
  load_dotenv()
  token = os.getenv('BT_TOKEN')
  parser = argparse.ArgumentParser(description='Программа позволяет сокращать ссылки и считать переходы по ним')
  parser.add_argument('link', help='Введи ссылку')
  args = parser.parse_args()

  try:
    link = args.link
    if test_link(token, link):
      count = count_clicks(token, link)
      print(f"Количество кликов {count}")
    else:
      print(shorten_links(token, link))
  except:
      print("какая-то ошибка")

if __name__ == '__main__':
  main()
