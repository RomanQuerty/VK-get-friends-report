import os
import logging
import re


"""
This module implements logic of creation report
"""

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def date_string_to_ISO_format(date_string):
    # VK date can be in two formats: d.m, or d.m.yyyy
    # We check both and format it in ISO
    # ATTENTION: Always check date with year first, because
    # date without year pattern will match both with and without year
    date_with_year_pattern = r'(\d*)\.(\d*)\.(\d*)'
    date_wo_year_pattern = r'(\d*)\.(\d*)'
    match = re.search(date_with_year_pattern, date_string)
    if match:   # If date with year
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
        date_with_year = True
    else:       # If date without year
        match = re.search(date_wo_year_pattern, date_string)
        if not match:
            raise Exception(f"Wrong date recived: {date_string}")
        day = match.group(1)
        month = match.group(2)
        date_with_year = False
    if len(day) == 1:   # If day is 1-char str we should add '0' before
        day = f'0{day}'  # number. Same with month
    if len(month) == 1:
        month = f'0{month}'
    if date_with_year:
        return f'{year}-{month}-{day}'  # ISO format yyyy-mm-dd
    else:
        return f'{month}-{day}'  # ISO format mm-dd


def create_report(vk_api_handler, offset=0):
    """
    This method gets raw VK data and changes it according report
    structure (skipping deleted and banned accounts). Each report is
    one processed request.
    e.g. raw vk friends data:
        {
            "response":{
            "count":1175
            "items":[
                0:{
                "id":126026250
                "deactivated":"banned"
                "first_name":"Πавел"
                "last_name":"Μаксимов"
                "track_code":"4be6a67e6sLKi..."
                }
                1:{
                "id":106503332
                "first_name":"Akio"
                "last_name":"Switch"
                "can_access_closed":false
                "is_closed":true
                "track_code":"e072771fcSu3l..."
                }
            ]
        }
    processed friends data:
    [
        {
            "First name": "Akio",
            "Last name": "Switch",
            "Country": "Россия",
            "City": "Москва",
            "Birthdate": "Нет данных",
            "Sex": "Male"
        }
    ]
    """
    # This function contains pretty big if/else construction,
    # but I think it is still more understandable and easy to
    # change, then using lot of different functions for each case.
    # BTW, we can't create universal "set_value" function, because
    # values are too different (e.g. look at city, bdate and sex).
    raw_friends_data = vk_api_handler.get_friends_data(offset)
    processed_friends_list = []
    for raw_friend_data in raw_friends_data:
        # We skip deleted and deactivated users
        if raw_friend_data['first_name'] == 'DELETED' or \
                'deactivated' in raw_friend_data:
            continue
        processed_friend_data = {
            'First name': raw_friend_data['first_name'],
            'Last name': raw_friend_data['last_name']
        }
        # Default country, city, bdate, sex value
        country = city = bdate = sex = 'No data'
        # Country
        if 'country' in raw_friend_data:
            country = raw_friend_data['country']['title']
        processed_friend_data['Country'] = country
        # City
        if 'city' in raw_friend_data:
            city = raw_friend_data['city']['title']
        processed_friend_data['City'] = city
        # Birthdate
        if 'bdate' in raw_friend_data:
            bdate = date_string_to_ISO_format(raw_friend_data['bdate'])
        processed_friend_data['Birthdate'] = bdate
        # Sex
        if 'sex' in raw_friend_data:
            if raw_friend_data['sex'] == 1:
                sex = 'Female'
            elif raw_friend_data['sex'] == 2:
                sex = 'Male'
            else:
                sex = 'Any'
        processed_friend_data['Sex'] = sex
        processed_friends_list.append(processed_friend_data)
    return processed_friends_list


def create_and_save_reports(vk_api_handler, saver):
    logging.info('Started report creation')
    friends_amount = vk_api_handler.get_friends_amount()
    logging.info(f'Friends amount got {friends_amount}')
    # we will use saved_friends as offset for create_report function
    saved_friends = 0
    while saved_friends < friends_amount:
        cls()
        print(f'Saved {saved_friends}/{friends_amount} friends')
        friends_data = create_report(vk_api_handler, saved_friends)
        saver.save(friends_data)
        saved_friends += int(vk_api_handler.config['users_in_request'])
        logging.debug(f'Saved friends {saved_friends} from reporter')
    print(f'Successfully saved {friends_amount} friends data')
