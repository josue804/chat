
Hospital Chat
==========

Provides condition-based live-chat channels for hospital patients. No login required.

<a href="https://warm-depths-62159.herokuapp.com/chat" target="_blank">Live Demo</a>

## Installation

Set up the `hpc` databases.  The default database settings are
in `hpc/settings.py`.

Make sure you have `redis` installed and running.

Create a virtual environment for the project: 

    $ mkvirtualenv hpc

Install project dependencies:

    $ pip install -r requirements.txt

Export the Django settings module:

    $ export DJANGO_SETTINGS_MODULE=hpc.settings

Run the webserver:

    $ ./manage.py runserver

## Development

If you'd like to use Gulp to auto-compile your LESS, navigate to `chat/static/chat` to install the node
dependencies:

    $ npm install

And run Gulp to watch and compile LESS files:

    $ gulp
