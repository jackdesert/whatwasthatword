from flask import Flask
import requests, json
app = Flask(__name__)

defs = []
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
    print(results)
    firstResult = results[0]
    print(firstResult)
    senses = firstResult['senses']
    print(senses)
    firstSense = senses[0]
    print(firstSense)
    definition = firstSense['definition'][0]
    defs.append("%s: %s" % (word, definition))

    return('<br>'.join(reversed(defs)))


if __name__ == "__main__":
    # enable debug so errors will be displayed, and so new code will be reloaded
    app.debug = True
    app.run('0.0.0.0')
