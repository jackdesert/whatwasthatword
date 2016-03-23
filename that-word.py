from flask import Flask, request, render_template, make_response, url_for, redirect
from livereload import Server as LiveReloadServer
import requests, redis, json, uuid, datetime
from word import Word
app = Flask(__name__)

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
REDIS_CLIENT = redis.Redis(connection_pool=POOL)
MAX_STORAGE_INDEX = 99

@app.route("/api/search", methods=['POST'])
def search_api():
    wordstring = request.form.getlist('word')[0]
    word_data = Word(wordstring).data()
    word_data_json = json.dumps(word_data)

    if word_data['parts_of_speech']:
        shared_session_id = session_id()
        REDIS_CLIENT.lpush(shared_session_id, word_data_json)
        # Limit how many records a given user can store
        REDIS_CLIENT.ltrim(shared_session_id, 0, MAX_STORAGE_INDEX)

    # TODO Return an error explicitly if no parts_of_speech
    # TODO so that the error checking is cleaner on the EcmaScript end
    print(word_data)
    return word_data_json

@app.route("/forget")
def forget_words():
    shared_session_id = session_id()
    REDIS_CLIENT.delete(shared_session_id)
    return redirect('/')

@app.route("/forget_single/<wordstring>", methods=['DELETE'])
def forget_single_word(wordstring):
    shared_session_id = session_id()
    words_in_redis = REDIS_CLIENT.lrange(shared_session_id, 0, MAX_STORAGE_INDEX)

    found = 0

    for word_in_redis in words_in_redis:
        word_decoded = word_in_redis.decode('utf-8')
        entry = json.loads(word_decoded)
        if entry['word'] == wordstring:
            REDIS_CLIENT.lrem(shared_session_id, word_decoded)
            found += 1
    return "Removed %d instances of %s" % (found, wordstring)

@app.route("/")
def home_page():

    shared_session_id = session_id()

    #REDIS_CLIENT.flushall()
    words_in_redis = REDIS_CLIENT.lrange(shared_session_id, 0, MAX_STORAGE_INDEX)
    toString = lambda x : x.decode('utf-8')
    words_in_redis_strings = list(map(toString, words_in_redis))
    data = []
    for entry in words_in_redis_strings:
        data.append(json.loads(entry))

    if request.query_string:
        # Redirect to the root so it looks better to user
        response = make_response(redirect('/'))
    else:
        join_url = '%s?shared_session_id=%s' % (request.url_root, shared_session_id)
        response = make_response(render_template('index.jj2', data=data, join_url=join_url))

    # Set the expiration far into the future
    expires = datetime.datetime(3000, 1, 1)
    # Note that we are setting the shared session id even
    # if it is not changing.
    response.set_cookie('shared_session_id', shared_session_id, expires=expires)
    return response

#   def ip_address():
#       # Use ip address passed from nginx if available
#       #
#       # GOTCHA: Make sure you call this method with (),
#       # or the function will be shoved into redis instead of the ip address
#       return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

def session_id():
    # There are three ways to get a shared_session_id
    id_from_params = request.args.get('shared_session_id')
    id_from_cookie = request.cookies.get('shared_session_id')
    id_freshly_minted = uuid.uuid1().hex
    return id_from_params or id_from_cookie or id_freshly_minted

if __name__ == "__main__":
    # enable debug so errors will be displayed, and so new code will be reloaded
    app.debug = True
    #app.run('0.0.0.0')

    # app is a Flask object

    server = LiveReloadServer(app.wsgi_app)
    # server.watch
    server.serve(port=3956, host='0.0.0.0')
