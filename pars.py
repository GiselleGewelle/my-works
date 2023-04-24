from bs4 import BeautifulSoup
import requests
import csv
from multiprocessing import Pool


def get_html(url):
    response=requests.get(url)
    return response.text

def get_soup(html):
    soup=BeautifulSoup(html,"html.parser")
    return soup

def get_last_page(soup):
    pages=soup.find("ul",class_="pagination").find_all("a",class_="page-link")
    last_page=pages[-1].get("data-page")
    return int(last_page)

def get_1page_links(soup):
    links=[]
    container=soup.find("div",class_="table-view-list")
    items=container.find_all("div",class_="list-item")
    for item in items:
        a=item.find("a").get("href")
        link="https://www.mashina.kg/search/all"+a
        links.append(link)
    return links
url="https://www.mashina.kg/search/all"
html=get_html(url)
soup=get_soup(html)
# print(get_1page_links(soup))
last_page=get_last_page(soup)


def get_links():
    res=[]
    for i in range(1,15):
        url=f"https://www.mashina.kg/search/all/?page={i}"
        html=get_html(url)
        soup=get_soup(html)
        page_link=get_1page_links(soup)
        res.extend(page_link)
    return res
# print(get_links())

def get_data(soup):
    container=soup.find("div",class_="table-view-list")
    cars=container.find_all("div",class_="list-item")
    result=[]
    for car in cars:
        name=car.find("h2",class_="name").text.strip()

        try:
            img=car.find("img",class_="lazy-image").get('data-src')
        except:
            img="NO Img"
        price_div=car.find("div",class_="block price")
        price=price_div.find("p").find("strong").text
        ls=["year-miles","body-type","volume"]
        desc=" ".join(car.find("p",class_=x).text.strip() for x in ls)
        
        data={
            "name":name,"desc":desc,"price":price,"img":img,
        }
        result.append(data)
    return result
# print(get_data(soup))

def prepare_csv():
    with open("work.csv","w") as file:
        fieldnames=["№","Name","Description","Price","Image Url"]
        writer=csv.DictWriter(file,fieldnames)
        writer.writerow({
            "№":"№",
            "Name":"Name",
            "Description":"Description",
            "Price":"Price",
            "Image Url":"Image Url"
        })

count=1
def write_to_scv(data):
    with open("work.csv","a") as file:
        fieldnames=["№","Name","Description","Price","Image Url"]
        writer=csv.DictWriter(file,fieldnames)
        global count
        for car in data:
            writer.writerow({
            "№":count,
            "Name":car["name"],
            "Description":car["desc"],
            "Price":car["price"],
            "Image Url":car["img"]
            })
            count+=1
data=get_data(soup)
# write_to_scv(data)

def make_all(link):
    data=get_data
    write_to_scv(data)
    

def main():
    prepare_csv()
    links=get_links()
    with Pool(10) as p:
        p.map(make_all,links)

if __name__=="__main__":
    main()
             