from time import sleep

from code.UI import ui

print('Hello, user!')
while ui():
    sleep(2)
print('Goodbye, user!')