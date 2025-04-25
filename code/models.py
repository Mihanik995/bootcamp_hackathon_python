import json

from code.utils import execute_query, get_film_by_api


class Film:
    def __init__(self, title: str, description: str, genre: str, year: str, rating: float):
        execute_query(
            'create table if not exists films (id serial primary key, title varchar(50), description text, genre varchar(30), year varchar(10), rating float)')

        self.title = title
        self.description = description
        self.genre = genre
        self.year = year
        self.rating = rating

        self.id = self.save()

    def __repr__(self):
        return f"{self.id}. {self.title}, {self.year} - {self.genre}."

    def __str__(self):
        return f"{self.id}. {self.title}, {self.year} - {self.genre}.\n{self.description}\nIMDb rating - {self.rating}"

    @classmethod
    def get(cls, id):
        response = execute_query(f"select * from films where id={id}")
        if response:
            return cls(response[0][1], response[0][2], response[0][3], response[0][4], response[0][5])

    @classmethod
    def all(cls):
        response = execute_query(f"select * from films")
        if response:
            result = []
            for row in response:
                result.append(cls(row[1], row[2], row[3], row[4], row[5]))
            return result

    @classmethod
    def add_by_api(cls, title):
        return cls(**get_film_by_api(title))

    def save(self):
        if not execute_query(f"select * from films where description = '{self.description}'"):
            execute_query('insert into films(title, description, genre, year, rating) '
                          f"values ('{self.title}', '{self.description}', '{self.genre}', '{self.year}', {self.rating})")
        return execute_query(f"select id from films where title = '{self.title}'")[0][0]

    def update(self, title: str, description: str, genre: str, year: int, rating: float):
        if not execute_query(f"select * from films where id = {self.id}"):
            self.id = self.save()
        execute_query(f"update films "
                      f"set title = '{title}', description = '{description}', genre = '{genre}', "
                      f"year = '{year}', rating = {rating} where item_id = '{self.id}'")

    def delete(self):
        if execute_query(f"select * from films where id = {self.id}"):
            execute_query(f"delete from films where id = {self.id}")

    @staticmethod
    def create_backup():
        with open('films_backup.json', 'w') as file:
            film_list = []
            for film in Film.all():
                film_list.append({'title': film.title,
                                  'description': film.description,
                                  'genre': film.genre,
                                  'year': film.year,
                                  'rating': film.rating})
            json.dump(film_list, file)

    @staticmethod
    def load_from_backup():
        with open('films_backup.json', 'r') as file:
            film_list = json.load(file)
            for film in film_list:
                Film(**film)
