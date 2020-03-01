from xml.etree.ElementTree import Element

from modules.xml import get_unique_xml_element

class Episode(object):

    def __init__(self, item: Element):
        self.guid = get_unique_xml_element(item, 'guid').text
        self.title = get_unique_xml_element(item, 'title').text
        self.date = get_unique_xml_element(item, 'pubDate').text
        self.url = get_unique_xml_element(item, 'enclosure').get('url')

        self.file_name = self.url.split('/')[-1]
        self.file_extension = self.file_name.split('.')[-1]
		#Issues with mp3?updated=stuff
