from flask import Flask, render_template,request
from bs4 import BeautifulSoup
import pandas as pd
import ssl
import requests
import bs4
import json
app = Flask(__name__)

@app.route("/")
def index():
    url = "https://m.dailyhunt.in/news/india/english"
    headers = {
            'Agent-Encoding':'qzip,deflate,sdch',
            'Accept-Language':'en-IN,en:q=0.8 ',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36.',
            'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
            'Referer':'https://www.wikipedia.org/',
            'Connection':'keep-alive',

        }
    r=  requests.get(url,headers=headers)
    

    Soup =  BeautifulSoup(r.text, 'html.parser')
        

    
    imgV = []
    titleV = []
    timeV = []
    linkV = []
    summaryV = []


    for x in Soup.findAll("ul" , {'id':'newsHeadline'}):
        for y in x.findAll('li', {'class':'lang_en'}):
            title = y.find('h2')
            titleV.extend(title.text)
            link = y.find('a')["href"]
            base_url = "https://" + link[1::]
            linkV.append(link)

            img = y.find('img')["src"]
            imgV.append(img)
                
            summary = y.find('p')
            summaryV.append(summary.text)
        
                    

    data = zip(titleV,linkV,imgV,summaryV)
    return render_template('index.html', data = data)

@app.route("/article")
def cnews():
    url = "https://m.dailyhunt.in/news/india/english"
    headers = {
               'Agent-Encoding':'qzip,deflate,sdch',
                'Accept-Language':'en-IN,en:q=0.8 ',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36.',
                'Accept':'text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, */*;q=0.8',
                'Referer':'https://www.wikipedia.org/',
                'Connection':'keep-alive',

        }
    r=  requests.get(url,headers=headers)
    

    Soup =  BeautifulSoup(r.text, 'html.parser')

    linkV = []

    for x in Soup.findAll("ul" , {'id':'newsHeadline'}):
        link = x.find('a')["href"]
        base_url = "https://" + link[1::]
        linkV.extend(link)

  

    re = requests.get(linkV,headers=headers)
    soup2 = BeautifulSoup(re.content,'html.parser')
        
    heading = []
    art = []
    img = []



    for y in soup2.findAll('div',{'class':'details_data'}):
        for a in y.findAll('h1'):
            heading.extend(a.text)

        
    for y in soup2.findAll('div',{'class':'details_data'}):
        for x in y.findAll('figure'):
           image = x.find('img')["src"]
           img.append(image)

            
    for y in soup2.findAll('div',{'class':'details_data'}) : 
        for x in y.findAll("div",{"class":"data"}):  
            content = x.findAll('p')
            art.append(x.text)

    data2 = zip(heading,img,art,linkV)

    return render_template('content.html',data2=data2)
            


    if __name__ == "__main__":
        app.run(debug=True)



                                            