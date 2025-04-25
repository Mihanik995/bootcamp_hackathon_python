from utils import execute_query

class Film:
    def __init__(self, title: str, description: str, genre: str, year: int, rating: float):
        execute_query('create table if not exists film (id serial primary key, title varchar(50), description text, genre varchar(30), year smallint, rating float)')

        self.title = title
        self.description = description
        self.genre = genre
        self.year = year
        self.rating = rating

        self.id = self.save()

    @classmethod
    def get(cls, id):
        response = execute_query(f"select * from film where id={id}")
        if response:
            return cls(response[0][1], response[0][2], response[0][3], response[0][4], response[0][5])


    def save(self):
        if not execute_query(f"select * from film where title = '{self.title}'"):
            execute_query('insert into film(title, description, genre, year, rating) '
                          f"values ('{self.title}', '{self.description}', '{self.genre}', {self.year}, {self.rating})")
        return execute_query(f"select id from film where title = '{self.title}'")[0][0]



    def update(self, title: str, description: str, genre: str, year: int, rating: float):
        if not execute_query(f"select * from film where id = {self.id}"):
            self.id = self.save()
        execute_query(f"update menu_items "
                      f"set title = '{title}', description = '{description}', genre = '{genre}', "
                      f"year = {year}, rating = {rating} where item_id = '{self.id}'")

    def delete(self):
        if execute_query(f"select * from film where id = {self.id}"):
            execute_query(f"delete from film where id = {self.id}")