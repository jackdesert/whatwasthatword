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
                <div className="subtitle">A dictionary that remembers words you&rsquo;ve recently needed</div>
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
                <Word entry={entry} />
            )
        })

        return (
            <div className="wordList">
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
                    example = <div className="example" dangerouslySetInnerHTML={ htmlObject(entry.example) }></div>
                }else{
                    example = null
                }

                if (entry.synonyms){
                    synonyms = <div className="synonyms"><span className="synonym-label">synonyms:</span> {entry.synonyms.join(", ")}</div>
                }else{
                    synonyms = null
                }

                return (
                    <div className="part-of-speech-contents">
                        <div className="definition" dangerouslySetInnerHTML={ htmlObject(entry.definition) }></div>
                        {example}
                        {synonyms}
                    </div>
                )
            })
            return (
                <div className="part-of-speech-wrapper">
                    <div className="part-of-speech">{key}</div>
                    {individualEntries}
                </div>
            )
        })


        return (
            <div className={ toggle.toggle('word-wrapper') }>
                <div className="close-button" data-the-word={this.props.entry.word}><a href="/">x</a></div>
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
var data2 = [{'word':'Hello', 'pronunciation':{'ipa':'whee', 'mp3':'yess.mp3'}}]

React.render(
  <WholePage url="/api/search" />,
  document.getElementById('content')
)

$('.close-button').on('click', function(event){
    event.preventDefault()
    $.ajax({
        url: '/forget_single/' + event.currentTarget.dataset.theWord,
        type: 'DELETE',
        success: function(data) {
            // Hide this word locally (ideally we would re-stripe also)
            $(event.currentTarget).parents('.word-wrapper').hide()
        }.bind(this),
        error: function(xhr, status, err) {
            console.error(this.props.url, status, err.toString())
        }.bind(this)
    })
})

