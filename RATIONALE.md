Rationale
=========

Q: Why is this dictionary being built when there are other dictionaries out there?

A: Because I need something that remembers words I looked up so I can review them later


Q: Why use IP addresses to differentiate users?

A: It is the simplest thing. IP address plus user-agent would be more specific,
   but suffers from the downfall when using two different devices on the same
   home (or office) internet connection.


Q: Why is this a web app instead of a native app?

A: Of necessity, because Jack is in the sphere of web apps (little Java experience)
   And of convenience, only one app is required, and it will work on anything.


Q: Why are objects delivered to the front end as JSON instead of as fully rendered html?

A: Because I want more experience being smart about front end stuff. This may also reduce
   the size of the payload, since divs are created on the front end.


Q: Why is a custom JSON object being delivered to the front end (see doc/api.json)
   instead of delivering exactly what the upstream API (originally Pearson) delivers?

A: A custom JSON payload was developed to deliver exactly the pieces required to
   emulate the google dictionary. Namely, this means all definitions for a "noun"
   are grouped together, etc. But this was also done because the (originally Pearson)
   api gives back more than is actually used. By defining our own data format, we get
   exactly the fields we need, with good naming conventions, and we drop everything else.
   This means that the JSON stored in Redis and the JSON sent to the front end is compact
   and easy to use.


Q: Why using Redis instead of SQL?

A: This problem could be solved using SQL. But the attributes of a single word never need be
   updated individually, so it is convenient to store them as a JSON blob. This is
   considerably simpler than using a relational mapping where each word has many
   definitions, each definition has a part_of_speech, etc.


Q: Why is Redis used instead of some other key/value store?

A: Redis is simpler to set up than Riak. And there is beauty in Redis lists that is
   a bit beyond a basic key/value store.


Q: Why is this written in Python?

A: Ruby is just as good a choice, but Jack wants to brush up on his python skills.


Q: Why Python3 instead of Python2?

A: Because it is the future, and because so far all dependencies work just fine in Python3.


Q: Why is this written in Flask instead of Django?

A: Because it is intended as a lightweight application.



