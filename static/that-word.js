var oddOrEven = function () {
    var state = 'odd';
    var toggle = function (klass) {
        if (state === 'odd') {
            state = 'even';
        } else {
            state = 'odd';
        }
        return klass + ' ' + state;
    };
    return { 'toggle': toggle };
};

var toggle = oddOrEven();

var WholePage = React.createClass({
    displayName: 'WholePage',

    getInitialState: function () {
        console.log('data: ', thatWordData);
        return { data: thatWordData };
    },

    handleSearchSubmit: function (jsonData) {
        var existingWords = this.state.data;
        //var newComments = comments.concat([comment])
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            type: 'POST',
            data: jsonData,
            success: function (data) {
                if (Object.keys(data.suggestions).length > 0) {
                    var sortedWords = data.suggestions.sort(function (a, b) {
                        return a.toLowerCase().localeCompare(b.toLowerCase());
                    });
                    alert('Whoops! Nothing found for "' + data.word + '".\nSuggestions: \n  ' + sortedWords.join('\n  '));
                    return;
                } else if (Object.keys(data.parts_of_speech).length === 0) {
                    alert('Whoops! Nothing found for "' + data.word + '".');
                    return;
                }
                var copy = JSON.parse(JSON.stringify(this.state.data));
                copy.unshift(data);
                this.setState({ data: copy });
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    render: function () {
        return React.createElement(
            'div',
            { className: 'wrapper' },
            React.createElement(
                'h1',
                null,
                'WhatWasThatWord?'
            ),
            React.createElement(
                'div',
                { className: 'subtitle' },
                'A dictionary that doubles as a vocabulary list'
            ),
            React.createElement(SearchForm, { onSearchSubmit: this.handleSearchSubmit }),
            React.createElement(WordList, { data: this.state.data })
        );
    }
});

var SearchForm = React.createClass({
    displayName: 'SearchForm',

    handleSubmit: function (e) {
        e.preventDefault();
        var text = React.findDOMNode(this.refs.text).value.trim();
        if (!text) {
            return;
        }
        this.props.onSearchSubmit({ word: text });
        React.findDOMNode(this.refs.text).value = '';
    },
    render: function () {
        return React.createElement(
            'form',
            { className: 'search-form', onSubmit: this.handleSubmit },
            React.createElement('input', { type: 'text', placeholder: 'Which word?', ref: 'text' }),
            React.createElement('input', { type: 'submit', value: 'Grok' })
        );
    }
});

var WordList = React.createClass({
    displayName: 'WordList',

    render: function () {
        var entries = this.props.data.map(function (entry) {
            return React.createElement(Word, { entry: entry });
        });

        return React.createElement(
            'div',
            { className: 'wordList' },
            entries
        );
    }
});

var Word = React.createClass({
    displayName: 'Word',


    render: function () {

        var pos = this.props.entry.parts_of_speech;
        var keys = [];

        for (var key in pos) {
            if (pos.hasOwnProperty(key)) {
                keys.push(key);
            }
        }

        var partsOfSpeech = keys.map(function (key) {
            var individualEntries = pos[key].map(function (entry) {
                var htmlObject = function (text) {
                    //this is only here to use with dangerouslySetInnerHtml
                    return { '__html': text };
                };

                var example, synonyms;
                if (entry.example) {
                    example = React.createElement('div', { className: 'example', dangerouslySetInnerHTML: htmlObject(entry.example) });
                } else {
                    example = null;
                }

                if (entry.synonyms) {
                    synonyms = React.createElement(
                        'div',
                        { className: 'synonyms' },
                        React.createElement(
                            'span',
                            { className: 'synonym-label' },
                            'synonyms:'
                        ),
                        ' ',
                        entry.synonyms.join(", ")
                    );
                } else {
                    synonyms = null;
                }

                return React.createElement(
                    'div',
                    { className: 'part-of-speech-contents' },
                    React.createElement('div', { className: 'definition', dangerouslySetInnerHTML: htmlObject(entry.definition) }),
                    example,
                    synonyms
                );
            });
            return React.createElement(
                'div',
                { className: 'part-of-speech-wrapper' },
                React.createElement(
                    'div',
                    { className: 'part-of-speech' },
                    key
                ),
                individualEntries
            );
        });

        return React.createElement(
            'div',
            { className: toggle.toggle('word-wrapper') },
            React.createElement(
                'div',
                { className: 'close-button', 'data-the-word': this.props.entry.word },
                React.createElement(
                    'a',
                    { href: '/' },
                    'x'
                )
            ),
            React.createElement(
                'div',
                { className: 'the-word' },
                this.props.entry.word
            ),
            React.createElement(
                'div',
                { className: 'pronunciation' },
                React.createElement(
                    'div',
                    { className: 'ipa inline' },
                    '/',
                    this.props.entry.pronunciation.ipa,
                    '/'
                ),
                React.createElement(
                    'div',
                    { className: 'mp3 inline' },
                    React.createElement(
                        'a',
                        { href: this.props.entry.pronunciation.mp3 },
                        React.createElement('img', { src: speakerImageSrc })
                    )
                )
            ),
            partsOfSpeech
        );
    }
});

// Note the React.render call needs to come after other things are defined.
var data2 = [{ 'word': 'Hello', 'pronunciation': { 'ipa': 'whee', 'mp3': 'yess.mp3' } }];

React.render(React.createElement(WholePage, { url: '/api/search' }), document.getElementById('content'));

$('.close-button').on('click', function (event) {
    event.preventDefault();
    $.ajax({
        url: '/forget_single/' + event.currentTarget.dataset.theWord,
        type: 'DELETE',
        success: function (data) {
            // Hide this word locally (ideally we would re-stripe also)
            $(event.currentTarget).parents('.word-wrapper').hide();
        }.bind(this),
        error: function (xhr, status, err) {
            console.error(this.props.url, status, err.toString());
        }.bind(this)
    });
});