import os
import logging


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_and_save_report(vk_api_handler, saver):
    logging.info('Started report creation')
    friends_amount = vk_api_handler.get_friends_amount()
    logging.info(f'Friends amount got {friends_amount}')
    saved_friends = 0  # we will use saved_friends as offset for
    prefix = 1         # get_friends_data_list function
    while saved_friends < friends_amount:
        cls()
        print(f'Saved {saved_friends}/{friends_amount} friends')
        friends_data = vk_api_handler.get_friends_data_list(saved_friends)
        saver.save(friends_data, prefix)
        prefix += 1
        saved_friends += int(vk_api_handler.config['users_in_request'])
    print(f'Successfully saved {friends_amount} friends data')
