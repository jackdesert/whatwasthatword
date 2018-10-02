What Was that Word
==================

A dictionary app that stores your history, effectively doubling as a vocabulary list.


Live on the Web
---------------

http://dictionary.jackdesert.com



Features
--------

### No Login Required

No login is required. Users are differentiated by a cookie stored during their first visit.


### Share Your List Across Browsers and Devices

Take your cookie with you to bridge other browsers together.
(Look for the link at the bottom of the home page)

### Merriam-Webster Data

Pulls data from the free Merriam-Webster API



Technologies
------------

    back-end:    Python, Flask, uWSGI, Redis, lxml
    front-end:   ReactJS
    data-source: Merriam-Webster API (xml)


Directory Structure
-------------------

    .babelrc
    config/
    doc/          # Documentation, including API payloads and RATIONALE for decisions
    jsx/          # Edit these jsx files
    node_modules/ # Node modules are stored in source control to make deployment easy
    RATIONALE.md  # Why decisions were made
    README.md
    bin/          # Executable utilities
    static/       # JSX files are compiled and output here (Do not edit manually)
    templates/    # jinja2 templates
    that-word.py  # Python script that runs site
    word.py       # Python class for interacting with dictionary API


Installation
------------

Install python3, pip3, and required python modules:

    # Build Dependencies
    sudo apt-get build-dep -y python3-lxml

    # Packages
    sudo apt-get install -y redis-server python3 python3-pip python3-setuptools

    # Python Modules
    pip3 install --user flask livereload requests redis lxml

    # Npm libraries (Skip this if /node_modules and package.json are in git)
    # See https://babeljs.io/docs/plugins/preset-react/
    npm install --save-dev babel-cli babel-preset-react



Development
-----------

In development mode:

  * JavaScript libraries are served from local disk
  * LiveReload is automatically activated
  * Code is loaded automatically when it changes

    cd whatwasthatword/

    # Start server
    python3 whatwasthatword.py

    # Compile .jsx files to .js whenever they change
    npx babel --presets react --watch jsx/ --out-dir static/

Point your browser to localhost:3956


Commonly Edited Files:

    * jsx/that-word.js
    * templates/index.jj2
    * word.py
    * that-word.py

Generated Files (Do Not Edit Manually):

    * static/that-word.js


Nginx
-----

If using in production, configure Nginx

    cd whatwasthatword/
    vi config/whatwasthatword-nginx.conf  # Set the server names you wish to use
    cd /etc/nginx/sites-enabled
    sudo ln -s /path/to/whatwasthatword/config/whatwasthatword-nginx.conf
    sudo nginx -s reload



uWSGI
-----

The unix socket must readable/writable by both nginx and uwsgi.

The easiest solution is to make sure both nginx and uwsgi run as the same user (www-data).

    # Install uwsgi and python3 plugin
    sudo apt install uwsgi-core uwsgi-plugin-python3

    # Install required python modules system-wide (So www-data can access them)
    sudo apt-get install python3-flask python3-livereload python3-redis python3-lxml

    # Test uwsgi from the command line running as the www-data user
    cd whatwasthatword
    sudo uwsgi --plugin=python3 -s /tmp/whatwasthatword.sock --manage-script-name --mount /=wsgi:app --uid www-data --gid www-data


Emperor
-------

(Work in Progress)

Ideally, you want uWSGI to autostart.


TODO
----

  * Run via emperor
  * Either all single or all double quotes in source code
  * Run over httpS / let's encrypt
  * Clean README
  * Get "share with other browser" to work (livereload showing up)


  * Assign stripe colors via css ::even to avoid striping errors on delete
  * Clean Python
  * Better organization of README
  * Copy-and-pastable "Share with other browser" link (Currently doesn not allow copy)


  * Play mp3 inline, instead of it loading a new webpage
  * return "vietnam" as "Vietnam", but still prefer lower case words if available
  * Expansion for more info?
  * Great Favicon
  * Show that word is being fetched
  * Autofocus search bar
  * Optimize padding breakpoint for android phones
  * Make input bigger on phone
  * Make speaker display correct size android
  * When I type "looking" I want results for "look", since that is what api returns
  * Spellchecker in text box
  * Clean up the <dt> tag processing to use the elegance of xpath more coherently
  * When more than one example per definition, show them all. Example: "snobby"
  * Remove "as" from the definition of "jack", or find out what it is there for
  * Make it autoplay the .mp3 for anything you search
  * Capitalization: when input is "Run", I want the word to display as "run". When word is "greek", display "Greek"
  * Allow plurals to be singularized and match
  * Better pronunciation for word "Oedipus"
  * Get "twirp" to work (twerp works fine)
  * Fix so that after hitting "back" from listening to mp3, most recent word shows up
  * Get word "were" to work (definition is buried in the etymology)
  * Longer cookie expiration

