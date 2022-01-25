from display_handler import ConsoleApp
import logging

if __name__ == "__main__":
    # Change log level to logging.DEBUG, if you want more info
    logging.basicConfig(filename='logs.log', level=logging.INFO)
    logging.info('Program started')
    app = ConsoleApp()
    app.main_screen()
