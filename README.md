Dick
====

Dick:

  * Isn't very smart
  * Uses the dictionary A LOT
  * Doesn't learn the word by only looking it up once
  * Wants a place that remembers what he looked up yesterday, and the day before, like a study list


Imagine this User Experience:



    --------------------------   ----------
    |   type next word here   |  | Search |
    --------------------------   ----------

    enrich: improve or enhance the quality or value of

    PREVIOUS WORDS:

        gaggle: a flock of geese
        noise: a sound, especially one that is loud or unpleasant or that causes disturbance
        petulant: (of a person or their manner) childishly sulky or bad-tempered
        obstinate: stubbornly refusing to change one's opinion or chosen course of action...
        nirvana: (in Buddhism) a transcendent state in which there is neither suffering...



Notes on User Experience:

  * cursor automatically focuses in search box
  * enter key submits search
  * "enrich" is the word you just looked up
  * previous words are listed in reverse chronological order of when they were searched
  * successive searches load without page load
  * each definition starts minimized (12 word maximum or so), but can be expanded for full definition



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
