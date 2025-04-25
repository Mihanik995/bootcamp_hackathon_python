import random
import unittest
from faker import Faker

from code.models import Film
from code.utils import execute_query


class FilmTestCase(unittest.TestCase):
    def setUp(self):
        execute_query('drop table films')
        execute_query(
            'create table films (id serial primary key, title varchar(50), description text, '
            'genre varchar(30), year varchar(15), rating float, viewed bool default false)')
        self.fake = Faker()
        self.films = []
        for i in range(5):
            self.films.append(Film(self.fake.catch_phrase()[:50],
                                   self.fake.text(50),
                                   random.choice(["Comedy", "Horror", "Sci-Fi"]),
                                   self.fake.year(),
                                   random.random() * 5 + 5))

    def test_getFilm(self):
        self.assertEqual(self.films[0], Film.get(self.films[0].id))

    def test_getAllFilms(self):
        self.assertEqual(self.films, Film.all())

    def test_saveFilm(self):
        self.films[0].save()
        self.assertEqual(len(Film.all()), len(self.films))
        self.films.append(Film(self.fake.catch_phrase(),
                                   self.fake.text(),
                                   random.choice(["Comedy", "Horror", "Sci-Fi"]),
                                   self.fake.year(),
                                   random.random() * 5 + 5))
        self.assertEqual(len(Film.all()), len(self.films))

    def test_deleteFilm(self):
        self.films[0].delete()
        self.assertEqual(len(Film.all()), len(self.films) - 1)

    def test_updateFilm(self):
        new_description = self.fake.text()
        self.films[0].update(description=new_description)
        self.assertEqual(Film.get(self.films[0].id).description, new_description)

    def test_changeViewed(self):
        self.films[0].change_viewed()
        self.assertEqual(Film.get(self.films[0].id).viewed, True)

    def tearDown(self):
        for film in self.films:
            film.delete()
