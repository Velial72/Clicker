import argparse
import requests
import os
from dotenv import load_dotenv


def is_bitlink(token, link):
  headers = {"authorization": token}
  check_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}'
  response = requests.get(check_url, headers=headers)
  result = response.ok
  return result


def shorten_links(token, link):
  bitlink_url = 'https://api-ssl.bitly.com/v4/shorten'
  body = {"long_url":  link}
  headers = {"authorization": token}
  response = requests.post(bitlink_url, headers=headers, json=body)
  response.raise_for_status()
  bitlink = response.json()['link']
  return bitlink


def count_clicks(token, link):
  headers = {"authorization": token}
  count_url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
  respons = requests.get(count_url, headers=headers)
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
    if is_bitlink(token, link):
      count = count_clicks(token, link)
      print(f"Количество кликов {count}")
    else:
      print(shorten_links(token, link))
  except:
      print("какая-то ошибка")

if __name__ == '__main__':
  main()
