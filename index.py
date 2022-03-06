from flask import Flask, make_response, render_template, Response
from queue import Queue, Empty
from bs4 import BeautifulSoup
from time import sleep
from flask_apscheduler import APScheduler
import datetime
import re
import requests
import subprocess
from playwright.sync_api import sync_playwright


app = Flask(__name__)

sch = APScheduler()
sch.init_app(app)

subprocess.call("playwright install")

with sync_playwright() as p:
    browser = p.webkit.launch()
    page = browser.new_page()
    page.goto("https://nhentai.net")
    page.wait_for_timeout(10000)
    print(page.content())
    browser.close()

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

@sch.task('cron', id='datapop', second='*/20')
def datapop():
 
  today = datetime.datetime.now()
  tm = today.strftime('%a, %d %b %y %H:%M:%S GMT')
  print("============ DATA UPDATED ============")
  print(tm)
  data1 = {}
  url = requests.get('https://nhentai.net/search/?q=english+-guro+-amputee&page=1&sort=popular-today')
    
  soup = BeautifulSoup(url.content, 'html')
  contents = soup.find('div', attrs = {'class':'container index-container'})

#  f = open("main.xml", "w")
#  print('<?xml version="1.0" encoding="utf-8"?>\n<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\n<channel>\n<title>nhentai-api</title>\n<lastBuildDate>', tm, '</lastBuildDate>\n',file=f)
  a1 = '<?xml version="1.0" encoding="utf-8"?>\n<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">\n<channel>\n<title>nhentai-api</title>\n<lastBuildDate>', tm, '</lastBuildDate>\n'

  for content in contents :
    title1 = content.text
    link = content.a['href']
    title = re.sub(r'[@$&]+','', title1)
    konten = f"""<item>
  <title>{title}</title>
  <link>https://nhentai.net{link}</link>
</item>"""
#    print(konten, file=f)
    a2 = konten
    data1[title] = f"https://nhentai.net{link}"
  
  nl = "\n"
  print(data1)
  a3 = "\n</channel>\n</rss>" 
#  print("</channel>\n</rss>", file=f)
#  f.close()
  return f'''<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
<channel>
<title>nhentai-eng-api</title>
<lastBuildDate>{tm}</lastBuildDate>
{nl.join(f'<item>{nl} <title>{key}</title>{nl} <link>{value}</link>{nl}</item>' for key, value in data1.items())}
</channel>
</rss>
'''

@app.errorhandler(404)
def page_not_found(e):
 return '''
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
<hr />
<h1 style="text-align:center"><span style="font-size:48px">What are you expecting here ?</span></h1>

<hr />
<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px">There are no nude picts here :P</span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px"><img alt="" src="https://c.tenor.com/_4xCiEhhoZsAAAAd/dog-smile.gif" style="height:320px; width:320px" /></span></p>

<p style="text-align:center">&nbsp;</p>

<p style="text-align:center"><span style="font-size:20px">&gt;&gt;&gt;&nbsp;<strong><span style="background-color:#00ff00"><a href="/" style="background-color: #00ff00;">Home</a></span></strong>&nbsp;|&nbsp;<strong><span style="background-color:#00ff00"><a href="/rss" style="background-color: #00ff00;">nHentai English RSS</a></span>&nbsp;</strong>| <strong><span style="background-color:#00ff00"><a href="/rss-pop" style="background-color: #00ff00;">nHentai Today Popular RSS</a></span>&nbsp;</strong>&lt;&lt;&lt;&lt;</span></p>
'''

@app.route('/rss-pop')
def rsspop():
  return Response(datapop(), mimetype='text/xml')
  
#if __name__ == '__main__':
#  sch.start()
#  app.run()
