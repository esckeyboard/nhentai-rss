from flask import Flask, make_response, render_template, Response
from queue import Queue, Empty
from bs4 import BeautifulSoup
from time import sleep
from flask_apscheduler import APScheduler
import datetime
import re
import requests

app = Flask(__name__)
run_with_ngrok(app)

sch = APScheduler()
sch.init_app(app)

@sch.task('cron', id='data', second='*/20')
def data():
 
  today = datetime.datetime.now()
  tm = today.strftime('%a, %d %b %y %H:%M:%S GMT')
  print("============ DATA UPDATED ============")
  print(tm)
  data1 = {}
  url = requests.get('https://nhentai.net/search/?q=english+-guro+-amputee+-bbm&page=1')
  soup = BeautifulSoup(url.content, 'html')
  contents = soup.find('div', attrs = {'class':'container index-container'})

  
  a1 = '<?xml version="1.0" encoding="utf-8"?>\n<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\n<channel>\n<title>nhentai-api</title>\n<lastBuildDate>', tm, '</lastBuildDate>\n'

  for content in contents :
    title1 = content.text
    link = content.a['href']
    title = re.sub(r'[@$&]+','', title1)
    
    data1[title] = f"https://nhentai.net{link}"
  
  nl = "\n"
  
  return f'''<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title>nhentai-eng-api</title>
<lastBuildDate>{tm}</lastBuildDate>
{nl.join(f'<item>{nl} <title>{key}</title>{nl} <link>{value}</link>{nl}</item>' for key, value in data1.items())}
</channel>
</rss>
'''

@app.route('/')
def main():
  return '''
  <h1 style="text-align: center;"><strong>nHentai API</strong></h1>
  <p style="text-align: center;">please donate :&gt;</p>
  <p style="text-align: center;">&nbsp;</p>
  <p style="text-align: center;">&nbsp;</p>
  <p style="text-align: center;"><span style="background-color: #00ff00;"><a style="background-color: #00ff00;" href="/rss">nHentai RSS English</a></span></p>
  '''
@app.route('/rss')
def rss():
  return Response(data(), mimetype='text/xml')

if __name__ == '__main__':
  sch.start()
  app.run()
