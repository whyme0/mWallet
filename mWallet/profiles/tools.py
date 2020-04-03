from settings.settings import STATICFILES_DIRS
from accounts.models import Person
import json
import os


def create_download_files(pk):
    """
    This function create files and save in path at
    ../static/temp-files/ of parcticular django project
    """
    user = Person.objects.get(pk=pk)

    # three file formats
    as_txt = (
        f'Name: {user.first_name}\n',
        f'Middle name: {user.middle_name}\n',
        f'Surname: {user.last_name}\n',
        f'Email: {user.email}\n',
        f'Phone number: {user.phone_number.raw_input}\n',
        f'Living place: {user.living_place}\n',
        f'Birth date: {str(user.birth_date)}\n',
        f'Account created date: {str(user.created_date)}\n')
    as_csv = (
        'name,middle name,surname,email,phone number,'
        'living place,birth date,account created\n',
        f'{user.first_name},{user.middle_name},{user.last_name},'
        f'{user.email},{user.phone_number.raw_input},'
        f'{user.living_place},{str(user.birth_date)},{str(user.created_date)}',)
    as_json = {
        'name': user.first_name,
        'middle name': user.middle_name,
        'surname': user.last_name,
        'email': user.email,
        'phone number': user.phone_number.raw_input,
        'living place': user.living_place,
        'birth date': str(user.birth_date),
        'account created date': str(user.created_date), }

    # direct file creation
    path_txt = os.path.join(STATICFILES_DIRS[0], os.path.abspath('static/temp-files/person.txt'))
    path_csv = os.path.join(STATICFILES_DIRS[0], os.path.abspath('static/temp-files/person.csv'))
    path_json = os.path.join(STATICFILES_DIRS[0], os.path.abspath('static/temp-files/person.json'))

    with open(path_txt, 'w', encoding='utf-8') as current_file:
        for line in as_txt:
            current_file.write(line)
    with open(path_csv, 'w', encoding='utf-8') as current_file:
        for line in as_csv:
            current_file.write(line)
    with open(path_json, 'w', encoding='utf-8') as current_file:
        json.dump(as_json, current_file)
