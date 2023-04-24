from bs4 import BeautifulSoup
import requests
import csv

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
url=f"https://www.mashina.kg/search/all/?page={i}"
html=get_html(url)
soup=get_soup(html)


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

def prepare_csv():
    with open("cars.csv","w") as file:
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
    with open("cars.csv","a") as file:
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
def main():
    prepare_csv()
    i=1
    lol=last_page
    while True:
        url=f"https://www.mashina.kg/search/all/?page={i}"
        html=get_html(url)
        soup=get_soup(html)
        data=get_data(soup)
        write_to_scv(data)
        last_page=get_last_page(soup)
        print(f"Спарсили {i}/{last_page} страниц")
        if i==lol:
            break
        i+=1
main()