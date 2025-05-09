import json

from code.utils import execute_query, get_film_by_api


class Film:
    def __init__(self, title: str, description: str, genre: str, year: str, rating: float, viewed: bool = False):
        execute_query(
            'create table if not exists films (id serial primary key, title varchar(50), description text, '
            'genre varchar(30), year varchar(15), rating float, viewed bool default false)')

        self.title = title
        self.description = description
        self.genre = genre
        self.year = year
        self.rating = rating
        self.viewed = viewed

        self.id = self.save()

    def __repr__(self):
        return f"{self.id}. {self.title}, {self.year} - {self.genre}. {'Viewed' if self.viewed else 'Not viewed'}"

    def __str__(self):
        return (f"{self.id}. {self.title}, {self.year} - {self.genre}.\n{self.description}\n"
                f"IMDb rating - {self.rating}\n"
                f"{'Viewed' if self.viewed else 'Not viewed'}")

    def __eq__(self, other):
        return self.id == other.id and isinstance(other, Film)

    @classmethod
    def get(cls, id):
        response = execute_query(f"select * from films where id={id}")
        if response:
            return cls(response[0][1], response[0][2], response[0][3], response[0][4], response[0][5], response[0][6])

    @classmethod
    def all(cls, viewed_only = False, not_viewed_only=False):
        if viewed_only and not_viewed_only:
            raise ValueError("Both 'viewed_only' and 'not_viewed_only' cannot be True at the same time.")
        query = "select * from films"
        if viewed_only:
            query += " where viewed = true"
        elif not_viewed_only:
            query += " where viewed = false"
        response = execute_query(query + " order by id")
        if response:
            result = []
            for row in response:
                result.append(cls(row[1], row[2], row[3], row[4], row[5], row[6]))
            return result

    @classmethod
    def add_by_api(cls, title):
        return cls(**get_film_by_api(title))

    def save(self):
        if not execute_query(f"select * from films where title='{self.title}'"):
            execute_query('insert into films(title, description, genre, year, rating) '
                          f"values ('{self.title}', '{self.description}', '{self.genre}', '{self.year}', {self.rating})")
        return execute_query(f"select id from films where title = '{self.title}'")[0][0]

    def update(self,
               title: str = None,
               description: str = None,
               genre: str = None,
               year: str = None,
               rating: float = None,
               viewed: bool = None):
        if not execute_query(f"select * from films where id = {self.id}"):
            self.id = self.save()
        execute_query(f"update films "
                      f"set title = '{title if title else self.title}', "
                      f"description = '{description.replace('\'', '\'\'') if description
                      else self.description.replace('\'', '\'\'')}', "
                      f"genre = '{genre if genre else self.genre}', "
                      f"year = '{year if year else self.year}', "
                      f"rating = {rating if rating else self.rating}, "
                      f"viewed = {viewed if viewed else self.viewed} where id = {self.id}")

    def delete(self):
        if execute_query(f"select * from films where id = {self.id}"):
            execute_query(f"delete from films where id = {self.id}")

    def change_viewed(self):
        if not execute_query(f"select * from films where id = {self.id}"):
            self.save()
        self.viewed = True
        self.update(viewed=self.viewed)

    @staticmethod
    def show_statistics():
        films = Film.all(viewed_only=True)
        genres_viewed = dict()
        for film in films:
            genres = film.genre.split(', ')
            for genre in genres:
                if genre in genres_viewed.keys():
                    genres_viewed[genre] += 1
                else:
                    genres_viewed[genre] = 1

        max_viewed = 0
        for count in genres_viewed.values():
            if count > max_viewed:
                max_viewed = count

        genres_most_viewed = []
        for genre in genres_viewed.keys():
            if genres_viewed[genre] == max_viewed:
                genres_most_viewed.append(genre)

        print(f"You have viewed {len(films)} movies.\n"
              f"Most viewed genres: {', '.join(genres_most_viewed)}\n")



    @staticmethod
    def create_backup():
        with open('films_backup.json', 'w') as file:
            film_list = []
            if Film.all():
                for film in Film.all():
                    film_list.append({'title': film.title,
                                      'description': film.description,
                                      'genre': film.genre,
                                      'year': film.year,
                                      'rating': film.rating,
                                      'viewed': film.viewed})
            json.dump(film_list, file)

    @staticmethod
    def load_from_backup():
        with open('films_backup.json', 'r') as file:
            film_list = json.load(file)
            for film in film_list:
                for key, value in film.items():
                    if isinstance(value, str):
                        film[key] = value.replace('\'', '\'\'')
                Film(**film)
