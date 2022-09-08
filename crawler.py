import requests
import logging
import argparse
import mysql.connector
from colorama import Fore, Style
from bs4 import BeautifulSoup
from usp.tree import sitemap_tree_for_homepage

def main():
    isNew = parseArgs().new
    baseURL = input('Enter URL to crawl: ')
    URLSHash = {}
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword"
  )


    siteMapSearch(baseURL, URLSHash)
    urlSearch(baseURL, URLSHash)

def cleanURL(baseURL, tag):
    link = tag.get('href')
    if not not link and link[0] == '/':
        link = baseURL + link
    link = link.replace('www.', '')

    return link

def urlSearch(baseURL, URLSHash):
    reqs = requests.get(baseURL)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    for tag in soup.find_all('a'):
        link = cleanURL(baseURL, tag)
        if link not in URLSHash and link != '#':
            print(Fore.YELLOW + "[url] ", end='')
            print(Style.RESET_ALL, end='')
            link = link
            print(link)
            URLSHash[link] = link
        else:
            URLSHash[link] = link

def siteMapSearch(baseURL, URLSHash):
    tree = sitemap_tree_for_homepage(baseURL)
    urls = [page.url for page in tree.all_pages()]

    for url in urls:
        if url not in URLSHash:
            print(Fore.BLUE + "[sitemap] ", end='')
            print(Style.RESET_ALL, end='')
            print(url)
            URLSHash[url] = url
        else:
            URLSHash[url] = url

def parseArgs():
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=formatter)
    parser.add_argument('--new', dest='new', action='store_true')
    parser.set_defaults(new=False)
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    main()
