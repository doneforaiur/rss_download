from defusedxml import ElementTree
from urllib import request

from xml.etree.ElementTree import Element

class XmlElementNotFound(Exception):
    '''The exception that is raised when an XML element was not found.'''

class XmlElementNotUnique(Exception):
    '''The exception that is raised when an XML element is not unique.'''

def get_unique_xml_element(scope: Element, element: str) -> Element:
    elements = scope.findall(element)

    if len(elements) == 0:
        raise XmlElementNotFound(f'Could not find the <{element}> element.')
    elif len(elements) > 1:
        raise XmlElementNotUnique(f'There is more than one <{element}> element.')
    else:
        return elements[0]

def parse_remote_xml(url: str) -> Element:

    xml_string = request.urlopen(url).read()
    return ElementTree.fromstring(xml_string)
    