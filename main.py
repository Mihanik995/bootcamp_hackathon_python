from time import sleep

from code.UI import ui
from code.utils import execute_query

execute_query(
    'create table if not exists films (id serial primary key, title varchar(50), description text, '
    'genre varchar(30), year varchar(15), rating float)')
print('Hello, user!')
while ui():
    sleep(2)
print('Goodbye, user!')
