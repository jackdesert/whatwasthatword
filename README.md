Dick
====

Dick is a dictionary app that doubles as a vocabulary list.


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

No login is required. Users are differentiated by their public IP address.

Documentation
-------------

Additional documentation, including API payloads and rationale for design decisions
available in doc/

    cd doc/


Deployment
----------

Install python, pip, and required python modules:

    sudo apt-get build-dep -y python3-lxml
    sudo apt-get install -y redis-server python3 python3-pip easy_install
    sudo pip3 install flask livereload requests redis lxml

If using in production, configure Nginx

    cd dict/
    vi config/dick-nginx.conf  # Set the server names you wish to use
    sudo ln -s config/dick-nginx.conf /usr/local/nginx/conf/sites-enabled/dick-nginx.conf
    sudo nginx -s reload

Start Dick

    python3 dick.py

Point your browser to localhost:3956


TODO
----

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
