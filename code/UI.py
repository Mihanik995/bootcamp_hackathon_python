from code.models import Film

action_options = """
1. View movies list
2. Add new movie
3. Delete a movie

0. Quit
"""


def ui() -> bool:
    print(action_options)
    while True:
        try:
            user_input = int(input('Choose an option: '))
            if user_input < 0 or user_input > 3:
                print('Invalid input')
                continue
            break
        except ValueError:
            print('I need a number')
    match user_input:
        case 0:
            return False
        case 1:
            if Film.all():
                for film in Film.all():
                    print(film)
                    print()
            else:
                print('No movies found')
        case 2:
            Film.add_by_api(input('Enter movie title: '))
            Film.create_backup()
            print('Movie added')
        case 3:
            if Film.all():
                for film in Film.all():
                    print(film.__repr__())
                try:
                    user_input = int(input('Choose a movie: '))
                    if user_input not in [film.id for film in Film.all()]:
                        print('Invalid input')
                        return True
                    Film.get(user_input).delete()
                    Film.create_backup()
                    print('Movie deleted')
                except ValueError:
                    print('I need a number')
            else:
                print('No movies to delete')
        case _:
            print('I didn\'t get your input')
    return True
