// Add a key to each final output div
var generator = function(){
    var count = -1,
        newKey = function(){
            count += 1
            return count.toString()
        }
    return {newKey: newKey}
}()

var oddOrEven = function(){
    var state = 'odd'
    var toggle = function(klass){
        if (state === 'odd'){
            state = 'even'
        }else{
            state = 'odd'
        }
        return klass + ' ' + state
    }
    return { 'toggle' : toggle }
}

var toggle = oddOrEven()

var WholePage = React.createClass({
    getInitialState: function() {
    console.log('data: ', thatWordData)
        return {data: thatWordData };
    },

    handleSearchSubmit: function(jsonData) {
        var existingWords = this.state.data
        //var newComments = comments.concat([comment])
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: jsonData,
            success: function(data) {

                // Not Found
                if (Object.keys(data.suggestions).length > 0){
                    var sortedWords = data.suggestions.sort(function (a, b) {
                        return a.toLowerCase().localeCompare(b.toLowerCase())
                    })
                    alert('Whoops! Nothing found for "' + data.word + '".\nSuggestions: \n  ' + sortedWords.join('\n  '))
                    return
                }else if (Object.keys(data.parts_of_speech).length === 0){
                    alert('Whoops! Nothing found for "' + data.word + '".')
                    return
                }

                // Found!
                console.log('submitting ' + JSON.stringify(jsonData))

                // TODO Why make a copy of the data?
                var copy = JSON.parse(JSON.stringify(this.state.data))
                copy.unshift(data)
                this.setState({data: copy})
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString())
            }.bind(this)
        })
    },

    render: function() {
        return (
            <div className="wrapper">
                <h1>WhatWasThatWord?</h1>
                <div className="subtitle">A dictionary that doubles as a vocabulary list</div>
                <SearchForm onSearchSubmit={this.handleSearchSubmit} />
                <WordList data={this.state.data}/>
            </div>
        )
    }
})

var SearchForm = React.createClass({
    handleSubmit: function(e) {
        e.preventDefault()
        var text = React.findDOMNode(this.refs.text).value.trim()
        if (!text) {
          return
        }
        this.props.onSearchSubmit({word: text})
        React.findDOMNode(this.refs.text).value = ''
    },
    render: function() {
        return (
            <form className="search-form" onSubmit={this.handleSubmit}>
                <input type="text" placeholder="Which word?" ref="text" />
                <input type="submit" value="Grok" />
            </form>
        )
    }
})

var WordList = React.createClass({
    render: function() {
        var entries = this.props.data.map(function(entry){
            return (
                <Word entry={entry} key={ generator.newKey() } />
            )
        })

        return (
            <div className="wordList" >
              {entries}
            </div>
        )
  }
})


var Word = React.createClass({


    render: function() {


        var pos = this.props.entry.parts_of_speech
        var keys = []

        for (var key in pos){
            if (pos.hasOwnProperty(key)) {
                keys.push(key)
            }
        }

        var partsOfSpeech = keys.map(function(key){
            var individualEntries = pos[key].map(function(entry){
                var htmlObject = function(text){
                    //this is only here to use with dangerouslySetInnerHtml
                    return {'__html': text}
                }

                var example, synonyms
                if (entry.example){
                    example = <div className="example"  dangerouslySetInnerHTML={ htmlObject(entry.example) }></div>
                }else{
                    example = null
                }

                if (entry.synonyms){
                    synonyms = <div className="synonyms" ><span className="synonym-label">synonyms:</span> {entry.synonyms.join(", ")}</div>
                }else{
                    synonyms = null
                }

                return (
                    <div className="part-of-speech-contents"  key={ generator.newKey() }>
                        <div className="definition" key={ generator.newKey() } dangerouslySetInnerHTML={ htmlObject(entry.definition) }></div>
                        {example}
                        {synonyms}
                    </div>
                )
            })
            return (
                <div className="part-of-speech-wrapper"  key={ generator.newKey() }>
                    <div className="part-of-speech">{key}</div>
                    {individualEntries}
                </div>
            )
        })


        return (
            <div className={ toggle.toggle('word-wrapper') } >
                <div className="close-button" data-the-word={this.props.entry.word}><a href="#a-swing-and-miss!">x</a></div>
                <div className="the-word">
                    {this.props.entry.word}
                </div>

                <div className="pronunciation">
                    <div className="ipa inline">
                        /{this.props.entry.pronunciation.ipa}/
                    </div>
                    <div className="mp3 inline">
                        <a href={this.props.entry.pronunciation.mp3}>
                            <img src={speakerImageSrc} />
                        </a>

                    </div>
                </div>
                {partsOfSpeech}
            </div>
        )
  }
})

// Note the React.render call needs to come after other things are defined.
// var sample_data = [{'word':'Hello', 'pronunciation':{'ipa':'whee', 'mp3':'yess.mp3'}}]

React.render(
  <WholePage url="/api/search" />,
  document.getElementById('content')
)

// Call "on" from $('#content
$('#content').on('click', '.close-button', function(event){
    var url = '/forget_single/' + event.currentTarget.dataset.theWord
    console.log('Clicked Delete for url ' + url)
    event.preventDefault()
    $.ajax({
        url: url,
        type: 'DELETE',
        success: function(data) {
            // TODO Delete word from wordData and call React.render
            // so striping will match

            // Hide this word locally
            $(event.currentTarget).parents('.word-wrapper').hide()
        }.bind(this),
        error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString())
        }.bind(this)
    })
})

$('#crawler').hide()
