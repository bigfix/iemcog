#!/usr/bin/python
import xml.etree.ElementTree as ET

class File(object):
    def __init__(self, string):
        self.raw = string
        self.fixlets = []
        root = ET.fromstring(string)
        # root = xml.getroot()
        if root.tag != 'BES':
            raise InputError('Not a valid BES file')
        for child in root:
            if child.tag == 'Fixlet':
                self.fixlets.append(File.elementfactory(child))
            else:
                print "Unrecognized Element: " + child.tag

    @classmethod
    def fromfilename(cls, filename):
        "Initialize from a .bes file"
        return cls(open(filename, 'r').read())

    @classmethod
    def elementfactory(cls, element):
        if element.tag == 'Fixlet':
            return Fixlet(element)
        elif len(element) == 0 and element.text:
            return TextElement.fromxml(element)
        else:
            return Element(element)

    def printBES(self):
        print self.raw

class Element(object):
    def __init__(self, element):
        if not hasattr(self, 'plurals'):
            self.plurals = set()
        self.loadxmldata(element)

    def loadxmldata(self, element):
        plurals = self.plurals
        children = {}
        for child in element:
            if child.tag in plurals:
                if child.tag in children:
                    children[child.tag] += [File.elementfactory(child)]
                else:
                    children[child.tag] = [File.elementfactory(child)]
            else:
                children[child.tag] = File.elementfactory(child)
        self.children = children
        self.attributes = element.attrib
        self.text = element.text
        self.tag = element.tag

    def __getattr__(self, name):
        "Allow easier access to text-only nodes"
        for val in self.text_accessors:
            if name.lower() == val.lower():
                if val in self.children:
                    return self.children[val].text
                else:
                    return None
        
        return AttributeError

    def setattribute(self, name, value):
        self.attributes[name] = value

    def hasattribute(self, name):
        return name in self.attributes

    def haselement(self, name):
        return name in self.children

    def addrelevance(self, value):
        element = TextElement.fromstring('Relevance', value)
        if 'Relevance' in self.children:
            self.children['Relevance'] += [element]
        else:
            self.children['Relevance'] = [element]

class Fixlet(Element):
    def __init__(self, element):
        self.plurals = set(['Relevance', 'Action'])
        self.loadxmldata(element)
        self.text_accessors = set([
            'Title',
            'Description',
            'Category',
            'Source',
            'SourceID',
            'SourceReleaseDate',
            'SourceSeverity',
            'CVENames',
            'SANSID',
            'Domain'
            ])

class TextElement(Element):
    def __init__(self, tag, text, attributes):
        self.tag = tag
        self.text = text
        self.attributes = attributes

    @classmethod
    def fromxml(cls, element):
        return cls(element.tag, element.text, element.attrib)

    @classmethod
    def fromstring(cls, tag, text, attrs=None):
        return cls(tag, text, attrs)

    def settext(self, text):
        self.text = text

    def gettext(self):
        return self.text

# Test code
besfile = File.fromfilename('test/test.bes')
for fixlet in besfile.fixlets:
    print fixlet.tag
    print fixlet.title
    print fixlet.Description

    print ''
    print '== Relevance: =='
    fixlet.addrelevance('true')
    for relevance in fixlet.children['Relevance']:
        print relevance.text


