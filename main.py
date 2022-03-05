from flask import Flask, make_response, render_template, Response
from queue import Queue, Empty
from bs4 import BeautifulSoup
from time import sleep
from flask_apscheduler import APScheduler
import datetime
import re
import requests

app = Flask(__name__)

sch = APScheduler()
sch.init_app(app)

@sch.task('cron', id='data', second='*/20')
def data():
  today = datetime.datetime.now()
  tm = today.strftime('%a, %d %b %y %H:%M:%S GMT')
  print("============ DATA UPDATED ============")
  print(tm)
  url = requests.get('https://nhentai.net/search/?q=english+-guro+-amputee+-bbm&page=1')
  soup = BeautifulSoup(url.content, 'html')
  contents = soup.find('div', attrs = {'class':'container index-container'})

  f = open("main.xml", "w")
  print('<?xml version="1.0" encoding="utf-8"?>\n<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\n<channel>\n<title>nhentai-api</title>\n<lastBuildDate>', tm, '</lastBuildDate>\n',file=f)

  for content in contents :
    title1 = content.text
    link = content.a['href']
    title = re.sub(r'[@$&]+','', title1)
    konten = f"<item>\n  <title>{title}</title>\n  <link>https://nhentai.net{link}</link>\n</item>"
    print(konten, file=f)

  print("</channel>\n</rss>", file=f)
  f.close()
  return 

@app.route('/')
def main():
  return '''
    <a href="/rss">nHentai RSS</a>
    '''


@app.route('/rss')
def rss():
  xml = open("main.xml", "r") 
  return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
  sch.start()
  app.run()
