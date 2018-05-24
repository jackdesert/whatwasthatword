What Was that Word
==================

What Was that Word is a dictionary app that doubles as a vocabulary list.


Live on the Web
---------------

http://whatwasthatword.com


Technologies
------------

    back-end:    Python, Flask, Redis, lxml
    front-end:   ReactJS
    data-source: Merriam-Webster (xml) API


No Login Required
-----------------

No login is required. Users are differentiated by a cookie stored during their first visit.

Take your cookie with you to bridge other browsers together.


Documentation
-------------

Additional documentation, including API payloads and rationale for design decisions
available in doc/

    cd doc/


Deployment
----------

Install python3, pip3, and required python modules:

    # Build Dependencies
    sudo apt-get build-dep -y python3-lxml

    # Packages
    sudo apt-get install -y redis-server python3 python3-pip python3-setuptools

    # Python Modules
    pip3 install --user flask livereload requests redis lxml

    # Npm libraries
    # This next line was only required the first time---
    # Now those libraries are saved in source code so no need to
    # reinstall them
    npm install --save-dev babel-cli babel-preset-react



Directory Structure
-------------------

    .babelrc
    config/
    doc/
    jsx/         # Edit these jsx files
    node_modules/
    RATIONALE.md
    README.md
    script/
    static/      # JSX files are compiled and dropped here
    templates/   # jinja2 templates
    that-word.py # Python script that runs site
    word.py      # Old version of Python script



Development Mode
----------------


*Edit* files in jsx/
Run `babel` as shown below to generate files in static/


In development mode:

  * JavaScript libraries are served from local disk
  * Code is loaded automatically when it changes
  * LiveReload is automatically activated

    cd what-was-that-word/
    npx babel --presets react --watch jsx/ --out-dir static/
    python3 that-word.py

Point your browser to localhost:3956


Production Mode
---------------

If using in production, configure Nginx

    cd what-was-that-word/
    vi config/that-word-nginx.conf  # Set the server names you wish to use
    sudo ln -s config/that-word-nginx.conf /usr/local/nginx/conf/sites-enabled/that-word-nginx.conf
    sudo nginx -s reload

Start that-word

    python3 that-word.py

Point your browser to localhost:3956


TODO
----

  * Get babel running on localhost
  * Better documentation of how to install babel: first time and every time
  * Clean Python
  * Great README
  * Fix bug where deleting a word change
  * Adapt to run via systemd
  * Better organization of README


  * Play mp3 inline
  * return "vietnam" as "Vietnam", but still prefer lower case words if available
  * Expansion for more info?
  * Great Favicon
  * Show that word is being fetched
  * Autofocus
  * Make prod more robust by not autoreloading
  * Optimize padding breakpoint for android phones
  * Make input bigger on phone
  * Make speaker display correct size android
  * When I type "looking" I want results for "look", since that is what api returns
  * Spellchecker in text box
  * Clean up the <dt> tag processing to use the elegance of xpath more coherently
  * When more than one example per definition, show them all. Example: "snobby"
  * Remove "as" from the definition of "jack", or find out what it is there for
  * Make it autoplay anything you type
  * When input is "Run", I want the word to display as "run". When word is "greek", display "Greek"
  * Allow plurals to be singularized and match
  * Better pronunciation for Oedipus
  * Put it in my portfolio
  * Get "twirp" to work (twerp works fine)
  * Fix so that after hitting "back" from listening to mp3, most recent word shows up
  * Get "were" to work (definition is buried in the etymology,
  * Longer cookie expiration

DONE
----
  * 500, 404
  * Fixed so that words are persistent through server restarts
  * Do something sensible when searching for the word "vietnam", which has no part_of_speech
  * Show more than 10 words
  * Store only 100 words
  * Plain favicon to prevent 404
  * Clean up code so most of it lives in a class
  * Use a *reputable* dictionary, that has more sophisticated definitions, like merriam webster
  * Make sure if a word has two definitions under a single part_of_speech, that they both get displayed
    Which might involve finding a different API provider since Pearsons seems to only give one definition
    per part_of_speech.
  * Synonyms
  * what about these words: sheesh, crimeny, yikes
  * "snobby" and "snobbish" need <fw> tag integrated in order to work
  * "superfluous" needs <d_link> tag integrated to work. Similar to "snobby" above
  * If I misspell a word, tell me about it! (currently 500 response). Example: "snoby"
  * Add pronunciation and mp3 back in
  * Add a route for /reset that clears words for that user
