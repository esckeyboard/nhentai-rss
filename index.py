from flask import Flask, make_response, render_template, Response
from queue import Queue, Empty
from bs4 import BeautifulSoup
from time import sleep
from flask_apscheduler import APScheduler
import datetime
import re
import requests
import cloudscraper
import json

app = Flask(__name__)

sch = APScheduler()
sch.init_app(app)

session = requests.Session()
session.headers = ...
scraper = cloudscraper.create_scraper(sess=session)

@sch.task('cron', id='data', second='*/20')
def data():
 
  today = datetime.datetime.now()
  tm = today.strftime('%a, %d %b %y %H:%M:%S GMT')
  print("============ DATA UPDATED ============")
  print(tm)
  data1 = {}
  url = requests.get('https://nhentai.net/search/?q=english')
  
  soup = BeautifulSoup(url.content, 'html')
  contents = soup.find('div', attrs = {'class':'container index-container'})
  
  for content in contents :
    title1 = content.text
    link = content.a['href']
    title = re.sub(r'<[@$&]+>','', title1)
    
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

@sch.task('cron', id='datapop', second='*/20')
def datapop():
 
  today = datetime.datetime.now()
  tm = today.strftime('%a, %d %b %y %H:%M:%S GMT')
  print("============ DATA UPDATED ============")
  print(tm)
  data1 = {}
  url = requests.get('https://nhentai.net/search/?q=%22%22&sort=popular-today')
    
  soup = BeautifulSoup(url.content, 'html')
  contents = soup.find('div', attrs = {'class':'container index-container'})

  for content in contents :
    title1 = content.text
    link = content.a['href']
    title = re.sub(r'<[@$&]+>','', title1)

    data1[title] = f"https://nhentai.net{link}"
  
  nl = "\n"

  return f'''<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title>nhentai-todaypopular-feed</title>
<lastBuildDate>{tm}</lastBuildDate>
{nl.join(f'<item>{nl} <title>{key}</title>{nl} <link>{value}</link>{nl}</item>' for key, value in data1.items())}
</channel>
</rss>
'''

@app.errorhandler(404)
def page_not_found(e):
 return '''
<head>
 <title>Page Not Found</title>
</head>

<hr />
<h1 style="text-align:center"><span style="font-size:72px"><strong>404 Not Found</strong></span></h1>

<p style="text-align:center"><span style="font-size:20px">Where are you going ? There is nothing here...</span></p>

<hr />
<p>&nbsp;</p>

<p>&nbsp;</p>

<p style="text-align:center"><img alt="" src="https://c.tenor.com/nq76xNvyoYkAAAAd/construction-lol.gif" style="height:264px; width:424px" /></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px">&gt;&gt;&gt;&nbsp;<strong><span style="background-color:#00ff00"><a href="/" style="background-color: #00ff00;">Home</a></span></strong>&nbsp;|&nbsp;<strong><span style="background-color:#00ff00"><a href="/rss" style="background-color: #00ff00;">nHentai English RSS</a></span>&nbsp;</strong>|&nbsp;<strong><span style="background-color:#00ff00"><a href="/rss-pop" style="background-color: #00ff00;">nHentai Popular Today RSS</a></span></strong> | <strong><span style="background-color:#00ff00"><a href="/rss-pop" style="background-color: #00ff00;">About</a></span>&nbsp;</strong>&lt;&lt;&lt;&lt;</span></p>
'''
 
@app.route('/')
def main():
  return '''
<head>
 <title>nhentai-rss</title>
 <meta name="google-site-verification" content="E7EGcxY15RFa-8vkDHisEJWk-J_CPSdqeIhn3CRyfC0" />
</head>
<hr />
<h1 style="text-align:center"><span style="font-size:48px"><strong>nHentai API</strong></span></h1>

<hr />
<p>&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px">please donate :&gt;</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px"><a href="https://paypal.me/mohimronfirdaus" target="_self"><img alt="" src="https://c.tenor.com/oCxcur4d32wAAAAC/squidward-spare-change.gif" style="height:237px; width:300px" /></a></span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center">&nbsp;</p>

<hr />
<p style="text-align:center"><span style="font-size:20px">&gt;&gt;&gt;&nbsp;<strong><span style="background-color:#00ff00"><a href="/rss" style="background-color: #00ff00;">nHentai English RSS</a></span>&nbsp;</strong>| <strong><span style="background-color:#00ff00"><a href="/rss-pop" style="background-color: #00ff00;">nHentai Today Popular RSS</a></span></strong> |&nbsp;<strong><span style="background-color:#00ff00"><a href="/about" style="background-color: #00ff00;">About</a></span>&nbsp;</strong>&lt;&lt;&lt;</span></p>

<hr />
<p>&nbsp;</p>'''
 
@app.route('/rss')
def rss():
 return Response(data(), mimetype='text/xml')

@app.route('/about')
def about():
    return '''
<head>
 <title>nhentai-rss</title>
</head>

<hr />
<h1 style="text-align:center"><span style="font-size:48px">What are you expecting here ?</span></h1>

<hr />
<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px">There are no nude picts here :P</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px"><img alt="" src="https://c.tenor.com/_4xCiEhhoZsAAAAd/dog-smile.gif" style="height:320px; width:320px" /></span></p>

<p style="text-align:center"><span style="font-size:20px">Source code : <strong><u><a href="https://github.com/esckeyboard/nhentai-rss">Github</a></u></strong></span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px">&gt;&gt;&gt;&nbsp;<strong><span style="background-color:#00ff00"><a href="/" style="background-color: #00ff00;">Home</a></span></strong>&nbsp;|&nbsp;<strong><span style="background-color:#00ff00"><a href="/rss" style="background-color: #00ff00;">nHentai English RSS</a></span>&nbsp;</strong>| <strong><span style="background-color:#00ff00"><a href="/rss-pop" style="background-color: #00ff00;">nHentai Today Popular RSS</a></span>&nbsp;</strong>&lt;&lt;&lt;&lt;</span></p>
'''

@app.route('/rss-pop')
def rsspop():
  return Response(datapop(), mimetype='text/xml')
  
#if __name__ == '__main__':
#  sch.start()
#  app.run()
