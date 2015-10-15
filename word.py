import requests
from lxml import etree
import re
import pdb

class Word:
    URL = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=5df5392d-be97-4dc9-b79d-889371de0aa4"
    MAX_DEFS = 5
    def __init__(self, headword):
        self._headword = headword
        self._data = { 'word' : headword, 'parts_of_speech' : {}, 'pronunciation': {}, 'suggestions': [] }
    def data(self):
        self._run()
        return self._data
    def _run(self):
        self._fetch()
        self._grab_suggestions()
        if self._data['suggestions']:
            # If there are suggestions, there are no definitions, so return
            return
        self._remove_extraneous_entries()
        self._process_entries()
        self._trim()
    def _grab_suggestions(self):
        for suggestion in self.root.xpath('suggestion'):
            self._data['suggestions'].append(suggestion.text)
    def _trim(self):
        for part_of_speech, array in self._data['parts_of_speech'].items():
            # Only return MAX_DEFS definitions, since sometimes there are a LOT
            del array[self.MAX_DEFS:]
    def _fetch(self):
        url = self.URL % self._headword
        #print('requesting %s' % self._headword)
        r = requests.get(url)
        #print('completed  %s' % self._headword)
        content = r.content                       # type is 'bytes'
        self.root = etree.fromstring(content)
    def _remove_extraneous_entries(self):
        self.entries = []
        for entry in self.root:
            id = entry.get('id')
            # convert "run[2]" to "run"
            id_plain = re.sub('[^a-zA-Z]', '', id)
            if id_plain.lower() == self._headword.lower():
                self.entries.append(entry)
    def _process_entries(self):
        for entry in self.entries:
            self._process_entry(entry)
    def _process_entry(self, entry):
        # <def> DEFINITION_ELEMENT
        # <dt>  DEFINING_TEXT
        # <fl>  FUNCTIONAL_LABEL
        # <vi>  VERBAL_ILLUSTRATION
        # <sx>  SYNONYMOUS CROSS REF TARGET
        # <pr>  PRONUNCIATION

        part_of_speech = entry.xpath('fl')[0].text
        defining_texts = entry.xpath('def/dt')

        ipa_list = entry.xpath('pr')
        mp3_list = entry.xpath('sound/wav')
        if ipa_list:
            self._data['pronunciation']['ipa'] = ipa_list[0].text
        if mp3_list:
            mp3 = mp3_list[0].text
            mp3_link = 'http://media.merriam-webster.com/soundc11/%s/%s' % (mp3[0], mp3)
            self._data['pronunciation']['mp3'] = mp3_link

        definitions = []
        for defining_text in defining_texts:
            dt_data = {}
            # convert to string so embedded tags come too
            text = etree.tostring(defining_text).decode('utf-8')
            # Remove start <dt> tag
            text = re.sub('.*<dt>', '', text)
            # Remove end <dt> tag and anything after
            text = re.sub('</dt>.*', '', text)
            # Remove all synonyms from the "more"
            text = re.sub('<sx>.*', '', text)
            # Remove all examples from the "more"
            text = re.sub('<vi>.*', '', text)
            # remove leading or trailing colons, including whitespace
            text = re.sub('\A\s*:|:\s*\Z', '', text)

            # Merriam sometimes gives colons in the middle of definitions,
            # but they read more cleanly as semicolons
            text = re.sub(' :', '; ', text)

            dt_data['definition'] = text

            verbal_illustrations = defining_text.xpath('vi')
            for verbal_illustration in verbal_illustrations:
                # TODO Catch ALL examples instead of just the last one
                example = etree.tostring(verbal_illustration).decode('utf-8')
                # Remove start <vi> tag
                example = re.sub('.*<vi>', '', example)
                # Remove end <vi> tag and anything after
                example = re.sub('</vi>.*', '', example)
                dt_data['example'] = example

            synonym_targets = defining_text.xpath('sx')
            synonyms = []
            for target in synonym_targets:
                synonyms.append(target.text)
            if synonyms:
                dt_data['synonyms'] = synonyms
            definitions.append(dt_data)

        self._data['parts_of_speech'][part_of_speech] = definitions
