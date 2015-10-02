from flask import Flask, request, render_template
from livereload import Server as LiveReloadServer
import requests, json, redis
app = Flask(__name__)

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
REDIS_CLIENT = redis.Redis(connection_pool=POOL)
MAX_STORAGE_INDEX = 99

@app.route("/api/search", methods=['POST'])
def search_api():
    wordstring = request.form.getlist('word')[0]
    url = "https://api.pearson.com/v2/dictionaries/ldoce5/entries?headword=%s&apikey=bxM09RSxa7VFkARAAYJJ8XSw4XXavRsu" % wordstring
    print('requesting %s' % wordstring)
    r = requests.get(url)
    print('completed  %s' % wordstring)
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
        if 'part_of_speech' in result:
            part_of_speech = result['part_of_speech']
        else:
            part_of_speech = '???'

        headword = result['headword']


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

    #import pdb; pdb.set_trace();

    if word_object['parts_of_speech']:
        REDIS_CLIENT.lpush(ip_address(), word_object_json)
        # Limit how many records a given user can store
        REDIS_CLIENT.ltrim(ip_address(), 0, MAX_STORAGE_INDEX)

    # TODO Return an error explicitly if no parts_of_speech
    # TODO so that the error checking is cleaner on the EcmaScript end
    return word_object_json




@app.route("/")
def home_page():

    #REDIS_CLIENT.flushall()
    words_in_redis = REDIS_CLIENT.lrange(ip_address(), 0, MAX_STORAGE_INDEX)
    toString = lambda x : x.decode('utf-8')
    words_in_redis_strings = list(map(toString, words_in_redis))
    data = []
    for entry in words_in_redis_strings:
        data.append(json.loads(entry))

    return render_template('index.jj2', data=data)


def ip_address():
    # Use ip address passed from nginx if available
    #
    # GOTCHA: Make sure you call this method with (),
    # or the function will be shoved into redis instead of the ip address
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


if __name__ == "__main__":
    # enable debug so errors will be displayed, and so new code will be reloaded
    app.debug = True
    #app.run('0.0.0.0')

    # app is a Flask object

    server = LiveReloadServer(app.wsgi_app)
    # server.watch
    server.serve(port=5000, host='0.0.0.0')
