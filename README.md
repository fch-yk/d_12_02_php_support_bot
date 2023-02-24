# PHP Support

PHP support platform

## Prerequisites

Python 3.11 is required.

## Installation

- Download the project files.
- It is recommended to use [venv](https://docs.python.org/3/library/venv.html?highlight=venv#module-venv) for project isolation.
- Set up packages:

```bash
pip install -r requirements.txt
```

- Set up environmental variables in your operating system or in the .env file. The variables are:

  - `DEBUG` - a boolean that turns on/off debug mode (optional, `False` by default);
  - `SECRET_KEY` - a secret key for a particular Django installation (obligatory);
  - `ALLOWED_HOSTS` - a list of strings representing the host/domain names that this Django site can serve (obligatory when `DEBUG` is set to `False`);
  - `DATABASE` - a database address (obligatory), go [here](https://github.com/jacobian/dj-database-url) for more;
  - `TELEGRAM_TOKEN` - a telegram token for php support bot (obligatory);
  - `LANGUAGE_CODE` - a string representing the language code for this installation (optional, `ru-Ru` by default);

To set up variables in .env file, create it in the root directory of the project and fill it up like this:

```bash
DEBUG=True
SECRET_KEY=replace_me
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE=db.sqlite3
TELEGRAM_TOKEN=replace_me
LANGUAGE_CODE=en-us
```

- Create SQLite database:

```bash
python manage.py migrate
```

- Create a superuser:

```bash
python manage.py createsuperuser
```

## Usage

- Run a development server:

```bash
python manage.py runserver
```

- Go to [the admin site](http://127.0.0.1:8000/admin/) and fill the base;
- Go to [the home page](http://127.0.0.1:8000/).
- Start the bot:

```bash
python manage.py start_bot
```

## Project goals

The project was created for educational purposes.
It's a training group project for python and web developers at [Devman](https://dvmn.org).
