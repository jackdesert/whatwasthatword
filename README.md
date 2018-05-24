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
  * Code is loaded automatically when it changes
  * LiveReload is automatically activated

    cd whatwasthatword/

    # Start server
    python3 that-word.py

    # Compile changes to jsx files to javascript files
    npx babel --presets react --watch jsx/ --out-dir static/

Point your browser to localhost:3956


Commonly Edited Files:

    * jsx/that-word.js
    * templates/index.jj2
    * word.py
    * that-word.py

Generated Files (Do Not Edit Manually):

    * static/that-word.js


Production Deploy
-----------------

If using in production, configure Nginx

    cd whatwasthatword/
    vi config/that-word-nginx.conf  # Set the server names you wish to use
    sudo ln -s config/that-word-nginx.conf /usr/local/nginx/conf/sites-enabled/that-word-nginx.conf
    sudo nginx -s reload

Start that-word

    python3 that-word.py

Point your browser to localhost:3956


TODO
----

  NOTES:  first click on "my" issues page reload instead of REDIS_CLIENT.lrem
  * Fix bug where deleting a word change
    - where / is / my / coat
    - delete "my"
  * Either all single or all double quotes
  * systemd


  * Assign stripe colors via css ::even to avoid striping errors on delete
  * Clean Python
  * Great README
  * Adapt to run via systemd
  * Better organization of README
  * Get items to show up in order they were typed in


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
