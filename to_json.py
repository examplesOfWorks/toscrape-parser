import json
from parser import get_quotes

all_quotes = []

# получение всех цитат и добавление их в список
for quote in get_quotes():
    all_quotes.append(quote)
    print(quote)

# запись списка с цитатами в файл
with open('quotes.json', 'w', encoding='utf-8') as file:
    json.dump(all_quotes, file, indent=4)
