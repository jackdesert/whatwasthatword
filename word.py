import requests, json
from lxml import etree

class Word:
    URL = "http://www.dictionaryapi.com/api/v1/references/collegiate/xml/%s?key=5df5392d-be97-4dc9-b79d-889371de0aa4"
    def __init__(self, headword):
        self.headword = headword
        self.data = { 'word' : headword, 'parts_of_speech' : {} }
    def json(self):
        self._run()
        return json.dumps(self.data)
    def _run(self):
        self._fetch()
        self._remove_extraneous_entries()
        self._process_entries()
    def _fetch(self):
        url = self.URL % self.headword
        #print('requesting %s' % self.headword)
        r = requests.get(url)
        #print('completed  %s' % self.headword)
        content = r.content                       # type is 'bytes'
        self.root = etree.fromstring(content)
    def _remove_extraneous_entries(self):
        self.entries = []
        for entry in self.root:
            if entry.get('id') == self.headword:
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
        entry_data = {}
        part_of_speech = entry.xpath('fl')[0].text
        defining_texts = entry.xpath('def/dt')
        definitions = []
        for defining_text in defining_texts:
            dt_data = {}
            dt_data['definition'] = defining_text.text
            #
            verbal_illustrations = defining_text.xpath('vi')
            for verbal_illustration in verbal_illustrations:
                # TODO Catch ALL examples instead of just the last one
                example = etree.tostring(verbal_illustration).decode('utf-8')
                # Remove enclosing <vi></vi> tags
                dt_data['example'] = example[4:-5]

            synonym_targets = defining_text.xpath('sx')
            synonyms = []
            for target in synonym_targets:
                synonyms.append(target.text)
            if synonyms:
                dt_data['synonyms'] = synonyms
            definitions.append(dt_data)

        self.data['parts_of_speech'][part_of_speech] = definitions
