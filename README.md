# Personal finance manager

## Description

This package provide HTTP-based user interface, that support such operations as:

- create asset, income or expense categories;
- create incoming or outgoing transactions.

Finanse logic calculates monthly expenses with based limit for each expense category (optional parameter) and show users their money overspending.  
Web functionality you might see on [the site](https://finance.py-exec.ru/).

Bot functionality available for telegram's user `@FinancePyexecTestBot`.  
And yes, it's still has testing state.

## Setup

1. checkout this repository into site's web-directory:

        cd /var/www/
        git clone https://github.com/ezhk/finance.git

2. check npm on your machine and build frontend:

        $ npm --version
        3.5.2
        $ cd finance/front
        $ npm i
        $ npm run build

3. create python enviroment and install deps and modules:

        $ python3 -mvenv /opt/venvs/finance
        $ source /opt/venvs/finance/bin/activate
        $ cd /var/www/finance
        $ pip install wheel
        $ pip install -r requirements.txt
        $ python3 setup.py install

4. define environment variables (or store them in `finance/confs/<filename>.ini`):

        $ cat finance/confs/secrets.ini
        [DEFAULT]
        SECRET_KEY = <SECRET KEY HERE>
        [BOT]
        TOKEN = <TG BOT TOKEN HERE>

    - DATABASE_PATH;
    - SECRET_KEY;
    - BOT_TOKEN.

5. create database:

        ./manage.py migrate

6. development run:

        ./manage.py runserver
        ./manage.py bot
        cd front && npm run serve

7. show `confs` directory as comfiguration exmaples for systemd and nginx.
