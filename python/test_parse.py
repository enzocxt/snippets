# -*- coding: utf-8 -*-

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


xml_text = """<pre>
   <code sentence-id="file:/Users/enzo/Projects/QLVL/other_tasks/corpus_convert/SoNaR/tmp/WR-P-P-G0000283.data.ids.xml">
      <file-id>WR-P-P-G-0000133582</file-id>
      <sentence>Pootjebaden aan de Haanstrakade</sentence>
 1      Pootjebaden     poot_DIM_baad   VERB    WW|inf|vrij|zonder      _       0       root    _       _
 2      aan     aan     ADP     VZ|init _       4       case    _       _
 3      de      de      DET     LID|bep|stan|rest       Definite=Def    4       det     _       _
 4      Haanstrakade    Haanstrakade    PROPN   SPEC|deeleigen  Number=Sing,Plur        1       nmod    _       _
          !
          </code>
</pre>"""


def show_et(xml_text):
    # tree = ET.parse(file=filename)
    root = ET.fromstring(xml_text)

    # get content after an xml item
    content = element.tail


class Sentence(object):
    def __init__(self, xml_text):
        root = ET.fromstring(xml_text)
        sentence_tag = 'sentence'
        sentence_item = self.find_rec(root, sentence_tag)
        sentence = sentence_item.tail.strip()
        # list of items
        self.items = self.parse_sentence(sentence)

    @classmethod
    def find_rec(cls, node, element):
        res = node.find(element)
        if res is None:
            for item in node:
                res = Sentence.find_rec(item, element)
        return res

    def parse_sentence(self, sentence):
        # check every line in sentence
        # if line does not start with a digit number (current lemma id)
        # it should be the last line with '!'
        lines = sentence.split('\n')
        lines = filter(lambda x: x[0].isdigit(), map(lambda x: x.strip(), lines))
        return lines


if __name__ == '__main__':
    so = Sentence(xml_text)
    print '\n'.join(so.items)
