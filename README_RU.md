# VK-get-friends-report

English version is in README.md file.

## Функции

* Отчет можно сохранить в csv, tsv и json форматах
* Можно легко добавить поддержку дополнительных форматов (например, YAML)
* Можно легко поменять структуру отчета (например добавить информацию про семейное положение)
* Код покрыт тестами
* Поддержка пагинации
* Поддержка большого количества данных и работы на компьютерах с малым количеством RAM.
* Есть логирование

---

## Установка и использование

### Зависимости

Python 3.8, requests 2.27.1

Скорее всего программа будет работать и на python 3.6+, но я это не гарантирую.

### Установка

Клонируйте репозиторий:

    git clone https://github.com/RomanQuerty/VK-get-friends-report.git

Установите зависимости:

    pip install -r requirements.txt


### Авторизация

Для работы с приложением Вы должны **вставить ваш ключ доступа в файл config.py**.

Вы можете получить ключ доступа перейдя по [этой ссылке](https://oauth.vk.com/authorize?client_id=8060115&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.131).
Ваш ключ будет сверху в url:

![Token example](README_images/token_from_browser.png)

Также Вы можете открыть страницу с авторизацией запустив скрипт:

    python3 get_access_token.py

Внимание! Ключ действителен только в течение 24 часов. По истечении суток вы должны получить новый ключ.

### Использование

Для запуска приложения запустите команду:

    python3 main.py

Вы можете поменять значение любого параметра (например id пользователя) в ходе выполнения самой программы. Если же Вы
хотите изменить значение параметра по умолчанию, вы можете сделать это в файле config.py.

### Использование на компьютерах с малых количеством RAM

Если у Вас сильно ограничено количество RAM вы можете уменьшить количество пользователей в запросе (amount of users in
single request.) Внимание! Чем меньше количество пользователей в запросе, тем дольше работает программа, т.к. надо
сделать больше запросов.

Хорошая особенность программы в том, что даже при малом количестве пользователей в запросе вы все ещё можете
создать большие отчеты в форматах csv и tsv, т.к. количество пользователей в файле не влияет на количество используемой
RAM. (К сожалению это не работает с json форматом)

---

## Добавление изменений

### Структура проекта

* `./README.md`:                 Английская версия этого файла.
* `./README_RU.md`:              Этот файл 
* `./config.py`:                 Конфигурационный файл со значениями параметров по умолчанию
* `./main.py`:                   Точка входа. Также в этом файле запускается логирование.
* `./get_access_token.py`:       Небольшой скрипт для открытия страницы авторизации.
* `./tests.py`                   Тесты. Реализованы при помощи стандартной библиотеки python **unittest**.
* `./libs/display_handler.py`:   Модуль, ответственный за пользовательский интерфейс.
* `./libs/vk_api_handler.py`:    Модуль, ответственный за взаимодействие с API Вконтакте. Реализован c помощью requests.
* `./libs/saver.py`:             Модуль, ответственный за сохранение данных.
* `./libs/report_creator.py`:    Модуль, реализующий логику создания отчетов. Использует методы VkApiHandler и Saver.


### Методы API Вконтакте, использованные в данном приложении

На самом деле, в приложении был задействован всего один метод API VK. Это [friends.get](https://dev.vk.com/method/friends.get).

Увидеть реализацию обращения к методу вы можете в файле libs/vk_api_handler.py.

### Запуск тестов

Для запуска тестов просто запустите команду:

    python3 tests.py

Модуль с тестами реализован на основе стандартной Python'овской библиотеки [unittest]((https://docs.python.org/3/library/unittest.html)),
так что вы легко можете добавить дополнительные тесты.

Я покрыл тестами почти все методы в основных случаях, однако осталось множество непокрытых случаев. Покрыть все случаи
не представляется возможным ввиду того, что получаемые из Вконтакте данные постоянно меняются.

### Что вы скорее всего захотите изменить

Коротко о том, с чего начать, если Вы хотите:

**Изменить структуру отчета** - взгляните на функцию *create_report* в файле *libs/report_creator.py*. Если Вам нужно
больше данных, получаемых от Вконтакте, измените значение **fields** в словаре **params** в методе *get_friends_data* в
файле *libs/vk_api_handler.py*.

**Добавить поддержку других типов данных** - инструкция, как это сделать приведена в docstring к классу Saver (файл *libs/saver.py*)

**Изменить пользовательский интерфейс приложения** - обратите внимание на методы класса **ConsoleApp's** оканчивающиеся 
на "*_screen*" (например, *main_screen*) в файле *libs/display_handler*.

**Изменить уровень логов** - просто поменяйте их в файле *main.py*.

### Оформление кода

Все оформление согласно [PEP8](https://www.python.org/dev/peps/pep-0008/).

Единственная вещь, которую следует уточнить, это **максимальная длина строки**.

Модули vk_api_handler, saver, tests и report_creator написаны с ограничением в 72 символа на строку.

Модуль display_handler написан с ограничением 99 символов на строку.

Уточнять ограничение для остальных файлов не имеет смысла.

---

## Обратная связь
Максим Новосельский

maxim.novoselsky@gmail.com

https://bitbucket.org/novoselsky

https://github.com/RomanQuerty