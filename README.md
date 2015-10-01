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
