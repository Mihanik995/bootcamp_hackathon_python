import os

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv(encoding='utf8', verbose=True)


def execute_query(query):
    with psycopg2.connect(host=os.getenv('HOST'),
                          port=os.getenv('PORT'),
                          user=os.getenv('USER'),
                          password=os.getenv('PASSWORD'),
                          database=os.getenv('DB')) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            try:
                return cursor.fetchall()
            except Exception as e:
                pass


def get_film_by_api(search_request):
    response = requests.get(url="http://www.omdbapi.com",
                            params={
                                "s": search_request,
                                "apikey": os.getenv('OMDB_API_KEY')
                            })
    print("Options I got:")
    options = []
    i = 0
    for option in response.json()['Search']:
        i += 1
        options.append([option['Title'], option['Year']])
        print(f"{i}. {option['Title']}, {option['Year']} - {option['Type']}")
        new_response = None
    while True:
        try:
            choice = int(input("Select an option: "))
            if choice <= 0 or choice > len(options):
                print("Invalid option")
                continue
            new_response = requests.get(url="http://www.omdbapi.com",
                                    params={
                                        "t": options[choice - 1][0],
                                        "y": options[choice - 1][1],
                                        "apikey": os.getenv('OMDB_API_KEY')
                                    })
            new_response = new_response.json()
            result = {'title': new_response['Title'],
                    'year': new_response['Year'],
                    'description': new_response['Plot'],
                    'genre': new_response['Genre'],
                    'rating': new_response['imdbRating']}
            for key, value in result.items():
                if isinstance(value, str):
                    result[key] = value.replace('\'', '\'\'')
            return result
        except ValueError:
            print('I need a number')
