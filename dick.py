from flask import Flask, request, render_template
import requests, json, redis
app = Flask(__name__)

defs = []
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redisClient = redis.Redis(connection_pool=pool)

@app.route("/")
def hello():
    r = requests.get("https://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=test&apikey=bxM09RSxa7VFkARAAYJJ8XSw4XXavRsu")
    return "Basic"


@app.route("/<wordstring>")
def printWord(wordstring):
    url = "https://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=%s&apikey=bxM09RSxa7VFkARAAYJJ8XSw4XXavRsu" % wordstring
    r = requests.get(url)
    content = r.content                       # type is 'bytes'
    contentString = content.decode('utf-8')
    myDict = json.loads(contentString)        # type is 'dict'
    results = myDict['results']

    word_object = { 'word' : wordstring, 'parts_of_speech' : {} }

    for result in results:
        if not result['senses']:
            # Some results have no senses
            continue
        if not result['headword'].lower() == wordstring.lower():
            # Some results are for compound words that include the headword
            continue
        if not 'part_of_speech' in result:
            # Some results do not name a 'part_of_speech' key
            continue

        part_of_speech = result['part_of_speech']


        headword = result['headword']

        #import pdb; pdb.set_trace();

        for sense in result['senses']:
            if not 'definition' in sense: continue
            # Note we only look for first definition
            definition_object = { 'definition' : sense['definition'][0] }
            if 'examples' in sense:
                definition_object['example'] = sense['examples'][0]['text']

            word_object['parts_of_speech'].setdefault(part_of_speech, []).append(definition_object)

        if 'pronunciations' in result:
            mp3 = "https://api.pearson.com%s" % result['pronunciations'][0]['audio'][0]['url']
            ipa = result['pronunciations'][0]['ipa']
            word_object['pronunciation'] = { 'ipa' : ipa, 'mp3' : mp3 }

    word_object_json = json.dumps(word_object)






    #for result in results:
    #    if result['senses']:
    #        resultsWithDefinitions.append(result)

    # Get ip from nginx if available
    ip_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    redisClient.lpush(ip_address, word_object_json)




    words_in_redis = redisClient.lrange(ip_address, 0, 10)
    toString = lambda x : x.decode('utf-8')
    words_in_redis_strings = list(map(toString, words_in_redis))
    data = []
    for entry in words_in_redis_strings:
        data.append(json.loads(entry))
    print(data)

    #redisClient.flushall()
    #return('<hr>'.join(words_in_redis_strings))
    return render_template('index.jj2', data=data)


if __name__ == "__main__":
    # enable debug so errors will be displayed, and so new code will be reloaded
    app.debug = True
    app.run('0.0.0.0')
