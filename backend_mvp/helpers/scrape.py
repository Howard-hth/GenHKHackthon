import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import project_environment as env

def page_retrival(category, sorted_data):
    # Send a GET request to the URL
    url = f'https://www.ninjiom.com/products/{category}?product=0'

    response = requests.get(url)
    html_content = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    tabs = soup.find_all('div', attrs={'role': 'tabpanel'})

    for tab in tabs:
        img = tab.find("img")["src"]
        sorted_data["img"].append(img)

        div = tab.find('div', class_='product-description px-8 pt-4')
        sorted_data["category"].append(category)
        sorted_data["product"].append(div.h4.text)
        sorted_data["description"].append(div.p.text)

        ingredient = tab.find_all('div', class_='h-8 sm:h-12 flex flex-col justify-center')  # Retrieves <p> inside <div>
        ingredient_list = []

        for index, div in enumerate(ingredient):
            if not index % 2:
                ingredient_list.append(div.text)
            else:
                ingredient_list[-1] += f"({div.text})"

        if ingredient_list:
            sorted_data["ingredient"].append(str(ingredient_list))
        else:
            sorted_data["ingredient"].append(str([sorted_data["description"][-1]]))

        if sorted_data["product"][-1] == "京都念慈菴蜜煉川貝枇杷膏（便利裝）":
            sorted_data["img"].pop()
            sorted_data["category"].pop()
            sorted_data["product"].pop()
            sorted_data["description"].pop()
            sorted_data["ingredient"].pop()

    return sorted_data

def scraper():
    sorted_data = {
        "img": [],
        "category": [],
        "product": [],
        "description": [],
        "ingredient": [] # (ingredient: purpose)
    }

    # prepare category map
    categories = []

    # URL of the webpage you want to scrape
    url = 'https://www.ninjiom.com/products/'

    # Send a GET request to the URL
    response = requests.get(url)
    html_content = response.text

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    divs = soup.find_all('div', class_='flex flex-row flex-wrap mb-8 justify-center')
    for index, div in enumerate(divs):
        type_list = div.find_all('a')
        type_name = type_list[0]['href'].split("/")[-1].split("?")[0]
        if type_name:
            categories.append(type_name)

    for category in categories:
        sorted_data = page_retrival(category, sorted_data)

    df = pd.DataFrame(sorted_data).drop_duplicates().reset_index(drop=True)

    # CONNECTION
    db_config = env.db_configs[env.db_mode]

    if db_config['dialect'] == 'sqlite':
        url = f"{db_config['dialect']}:///{db_config['database']}.db" # SQLite
    else:
        url = f"{db_config['dialect']}+{db_config['driver']}://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}" # MySQL

    engine = create_engine(url)
    conn = engine.connect()
    df.to_sql(name='NinJiom', con=engine, if_exists='replace', index_label='id')


def parse(list_str):
    list_str = list_str.split("['")[1:][0]
    list_str = list_str.split("']")[:-1][0]
    real_list = list_str.split("', '")

    return real_list