from code.models import Film

action_options = """
1. Show all movies list
2. Show not viewed movies list
3. Add new movie
4. Delete a movie
5. Mark movie as viewed
6. Restore movies list from backup
7. Show statistics

0. Quit
"""


def ui() -> bool:
    print(action_options)
    while True:
        try:
            user_input = int(input('Choose an option: '))
            break
        except ValueError:
            print('I need a number')
    match user_input:
        case 0:
            return False
        case 1:
            if Film.all():
                for film in Film.all():
                    print()
                    print(film)
            else:
                print('No movies found')
        case 2:
            if Film.all(not_viewed_only=True):
                for film in Film.all(not_viewed_only=True):
                    print()
                    print(film)
            else:
                print('No movies found')
        case 3:
            Film.add_by_api(input('Enter movie title: '))
            Film.create_backup()
            print('Movie added')
        case 4:
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
                print('No movies found')
        case 5:
            if Film.all(not_viewed_only=True):
                for film in Film.all(not_viewed_only=True):
                    print(film.__repr__())
                try:
                    user_input = int(input('Choose a movie: '))
                    if user_input not in [film.id for film in Film.all()]:
                        print('Invalid input')
                        return True
                    Film.get(user_input).change_viewed()
                    Film.create_backup()
                    print(f'Movie "{Film.get(user_input).title}" marked as viewed')
                except ValueError:
                    print('I need a number')
            else:
                print('No movies found')
        case 6:
            Film.load_from_backup()
            print('Movies loaded')
        case 7:
            Film.show_statistics()
        case _:
            print('I didn\'t get your input')
    return True
