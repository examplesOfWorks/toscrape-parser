from time import sleep
from requests import Session
from bs4 import BeautifulSoup
import dateparser

data = {
    "username": "username",
    "password": "password",
    "csrf_token": "csrf_token"
}

headers = { "User-Agent":
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",}

main_url = "https://quotes.toscrape.com/"

session = Session()
session.get(main_url, headers=headers)

login_response = session.get(main_url + "/login", headers=headers)
soup = BeautifulSoup(login_response.text, "lxml")
# получение токена для авторизации
csrf_token = soup.find("form").find("input").get("value")
data["csrf_token"] = csrf_token

# авторизация
page = session.post(main_url + "/login", headers=headers, data=data, allow_redirects=True)

# получение всех цитат для последующей записи их в json-файл
def get_quotes():
    
    count = 1
    while count > 0:
        main_url = f"https://quotes.toscrape.com/page/{count}/"
        quotes_response = session.get(main_url, headers=headers)
        sleep(2)
        quotes_soup = BeautifulSoup(quotes_response.text, "lxml")

        all_quotes = quotes_soup.find_all("div", class_="quote")
        
        if len(all_quotes) != 0:
            for quote in all_quotes:

                # получение текста цитаты
                text_of_quote = quote.find("span", class_="text").text.strip()

                # получение данных об авторе
                name_of_author = quote.find("small", class_="author").text.strip()
                author_url = quote.find("a").get("href")

                # получение информации об авторе
                author_about_data = session.get("https://quotes.toscrape.com/" + author_url, headers=headers) 
                author_about_soup = BeautifulSoup(author_about_data.text, "lxml")
                author_born_date = str(dateparser.parse(author_about_soup.find("span", class_="author-born-date").text.strip()))
                author_born_location = author_about_soup.find("span", class_="author-born-location").text.strip()
                author_description = author_about_soup.find("div", class_="author-description").text.strip()

                # получение тегов
                tags = quote.find("div", class_="tags").find_all("a", class_="tag")
                tags_list = []
                for tag in tags:
                    tags_list.append(tag.text.strip())

                yield {"text_of_quote": text_of_quote, "author": {"name_of_author": name_of_author, "author_born_date": author_born_date, "author_born_location": author_born_location, "author_description": author_description}, "tags": tags_list}
        else:
            break
       
        count += 1