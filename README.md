Dick
====

Dick is a dictionary app that doubles as a vocabulary list.


Live on the Web
---------------

http://whatwasthatword.com


Technologies
------------

    back-end:  Python, Flask, Redis
    front-end: ReactJS
    API:       Pearson Dictionary API


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

    sudo apt-get install -y redis-server python3 python3-pip easy_install
    sudo pip3 install flask livereload requests redis

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

  * Make sure if a word has two definitions under a single part_of_speech, that they both get displayed
    Which might involve finding a different API provider since Pearsons seems to only give one definition
    per part_of_speech.
  * Play mp3 inline
  * Report to Pearson that their mp3s only load half the time with error:
    "Server error: The difference between the request time and the current time is too large."
  * Teach it to show "Vietnam" (capitalized) when searching for "vietnam" (lowercase)
  * what about these words: sheesh, crimeny, yikes
  * Synonyms
  * Use a *reputable* dictionary, that has more sophisticated definitions, like merriam webster
  * Expansion for more info?
  * Get "looking" to show up
  * Great Favicon
  * Clean up code so most of it lives in a class
  * Show that word is being fetched
  * Autofocus
  * Make prod more robust by not autoreloading

DONE
----
  * 500, 404
  * Fixed so that words are persistent through server restarts
  * Do something sensible when searching for the word "vietnam", which has no part_of_speech
  * Show more than 10 words
  * Store only 100 words
  * Plain favicon to prevent 404
