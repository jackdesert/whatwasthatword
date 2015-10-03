from flask import Flask, request, render_template
from livereload import Server as LiveReloadServer
import requests, redis, json
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
        REDIS_CLIENT.lpush(ip_address(), word_data_json)
        # Limit how many records a given user can store
        REDIS_CLIENT.ltrim(ip_address(), 0, MAX_STORAGE_INDEX)

    # TODO Return an error explicitly if no parts_of_speech
    # TODO so that the error checking is cleaner on the EcmaScript end
    print(word_data)
    return word_data_json




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
    #server.serve(port=3956, host='0.0.0.0')
    server.serve(port=5000, host='0.0.0.0')
