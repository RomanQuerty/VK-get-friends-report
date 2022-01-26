# VK-get-friends-report

Русская версия находится в файле README_RU.md.

## Features

* Saving in csv, tsv and json format
* Easy to add new file types support
* Easy to change report structure (e.g. add relationship data)
* Covered with tests
* Pagination support
* Large Data support (works well on PC with lack of RAM)
* Logging support

---

## Installation and usage

### Dependencies

Python 3.8, requests 2.27.1

Probably it will work fine with python 3.6+, but I can't guarantee it.

### Installation

Clone repo:

    git clone https://github.com/RomanQuerty/VK-get-friends-report.git

Install requirements:

    pip install -r requirements.txt


### Authorization

For working with app you must **enter your access token in config.py** file.

You can get access token [here](https://oauth.vk.com/authorize?client_id=8060115&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131).
Copy token from url:

![Token example](README_images/token_from_browser.png)

You can also open auth page running:

    python3 get_access_token.py

Pay attention: token expires after 24 hours.

### Usage

Just run

    python3 main.py

You can change any parameter value (e.g. user id or output file name) in program. If you want to change default 
parameters value, you can simply do it in config.py file.



### Little RAM usage

If you have little RAM you should set less amount of users **in single request**. Pay attention: Less amount of users in
request also will make you program run slowly, because you need make more requests.

Cool feature: you still can create big csv or tsv files - amount of users **in file** doesn't depend on RAM
(unfortunately, it doesn't work with json format).

---

## Adding changes

### Project structure

* `./README.md`:                 This file.
* `./README_RU.md`               Russian version of this file.
* `./config.py`:                 Configuration file with default parameter values and VK APP ID.
* `./main.py`:                   Entry point. Also, it initializes logging.
* `./get_access_token.py`:       Little script opens VK auth page.
* `./tests.py`                   Tests. Based on python unittest lib.
* `./libs/display_handler.py`:   Module responsible for user interface and session parameters.
* `./libs/vk_api_handler.py`:    Module responsible for interaction with VK api. Uses requests.
* `./libs/saver.py`:             Module responsible for saving data.
* `./libs/report_creator.py`:    Module responsible for report structure. Depends on Saver and VkApiHandler.


### VK API methods used in this system

Actually, system uses only 1 VK API method. It's [friends.get](https://dev.vk.com/method/friends.get).

If you want to see this method usage look at vk_api_handler.py lib.

### Running tests

Run tests simply with:

    python3 tests.py

Test module based on [python unittest lib](https://docs.python.org/3/library/unittest.html), so you can easily add more
tests, if you need it.

I created tests for most of common cases, but there is still a lot of uncovered cases which hard to cover, because
data in VK changes often.

### Things you probably want to change

Quick guide where to start if you want to:

**Change report structure** - look at *create_report* function in *libs/report_creator.py*. If you need more data
received from VK add **fields** in **params** in *get_friends_data* method of **VkApiHandler** class
(*libs/vk_api_handler.py*).

**Add more file types support** - look instruction in Saver class docstring (*libs/saver.py*)

**Change app appearance** - look at **ConsoleApp's** methods ended with "*_screen*" (e.g. *main_screen* method) in
*libs/display_handler*.

**Change log level** - simple change level in *main.py*.

### Code style

Just follow [PEP8](https://www.python.org/dev/peps/pep-0008/).

Only thing that should be clarified is **line length**.

vk_api_handler, saver, tests and report_creator modules written with 72 line length limit.

display_handler written with 99 line length limit.

Set limitation for other files has no sense.

---

## Feedback
Maxim Novoselsky

maxim.novoselsky@gmail.com

https://bitbucket.org/novoselsky

https://github.com/RomanQuerty