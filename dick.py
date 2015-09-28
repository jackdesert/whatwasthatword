from flask import Flask, request
import requests, json, redis
app = Flask(__name__)

defs = []
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redisClient = redis.Redis(connection_pool=pool)

@app.route("/")
def hello():
    r = requests.get("https://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=test&apikey=bxM09RSxa7VFkARAAYJJ8XSw4XXavRsu")
    return "Basic"


@app.route("/<word>")
def printWord(word):
    url = "https://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=%s&apikey=bxM09RSxa7VFkARAAYJJ8XSw4XXavRsu" % word
    r = requests.get(url)
    content = r.content                       # type is 'bytes'
    contentString = content.decode('utf-8')
    myDict = json.loads(contentString)        # type is 'dict'
    results = myDict['results']

    # Only results that have senses
    results = list(filter(lambda x: x['senses'], results))

    # Keep only where headword matches exactly
    results = list(filter(lambda x: x['headword'].lower() == word.lower(), results))

    # Keep only where part_of_speech is given
    results = list(filter(lambda x: 'part_of_speech' in x, results))

    #for result in results:
    #    if result['senses']:
    #        resultsWithDefinitions.append(result)

    # Get ip from nginx if available
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    for result in results:
        part_of_speech = result['part_of_speech']
        headword = result['headword']
        for sense in result['senses']:
            if not 'definition' in sense: continue
            #import pdb; pdb.set_trace();
            for definition in sense['definition']:
                definitionWithWord = "%s (%s): %s" % (headword, part_of_speech, definition)
                redisClient.lpush(ip_address, definitionWithWord)

    #firstResult = results[0]
    #senses = firstResult['senses']
    #firstSense = senses[0]
    #definition = firstSense['definition'][0]
    #definitionWithWord = "%s: %s" % (word, definition)
    #defs.append(definitionWithWord)


    defsInRedis = redisClient.lrange(ip_address, 0, 10)
    toString = lambda x : x.decode('utf-8')
    defsInRedisStrings = list(map(toString, defsInRedis))

    return('<br>'.join(defsInRedisStrings))


if __name__ == "__main__":
    # enable debug so errors will be displayed, and so new code will be reloaded
    app.debug = True
    app.run('0.0.0.0')
