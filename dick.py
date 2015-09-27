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

    resultsWithDefinitions = []
    for result in results:
        if result['senses']:
            resultsWithDefinitions.append(result)

    firstResult = resultsWithDefinitions[0]
    senses = firstResult['senses']
    firstSense = senses[0]
    definition = firstSense['definition'][0]
    definitionWithWord = "%s: %s" % (word, definition)
    defs.append(definitionWithWord)
    # Get ip from nginx if available

    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    redisClient.lpush(ip_address, definitionWithWord)

    defsInRedis = redisClient.lrange(ip_address, 0, 10)
    toString = lambda x : x.decode('utf-8')
    defsInRedisStrings = list(map(toString, defsInRedis))
    #import pdb; pdb.set_trace();

    return('<br>'.join(defsInRedisStrings))


if __name__ == "__main__":
    # enable debug so errors will be displayed, and so new code will be reloaded
    app.debug = True
    app.run('0.0.0.0')
