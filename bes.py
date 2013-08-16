#!/usr/bin/python
import xml.etree.ElementTree as ET

class File:
    def __init__(self, string):
        self.raw = string
        self.fixlets = []
        root = ET.fromstring(string)
        # root = xml.getroot()
        if root.tag != 'BES':
            raise InputError('Not a valid BES file')
        for child in root:
            if child.tag == 'Fixlet':
                self.fixlets.append(Fixlet(child))
            else:
                print "Unrecognized Element: " + child.tag

    @classmethod
    def fromfilename(cls, filename):
        "Initialize from a .bes file"
        return cls(open(filename, 'r').read())

    def printBES(self):
        print self.raw

class Element:
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
                    children[child.tag] += [Element(child)]
                else:
                    children[child.tag] = [Element(child)]
            else:
                children[child.tag] = Element(child)
        self.children = children
        self.attributes = element.attrib
        self.text = element.text
        self.tag = element.tag

    def setattribute(self, name, value):
        self.attributes[name] = value

    def hasattribute(self, name):
        return name in self.attributes

    def haselement(self, name):
        return name in self.children

class Fixlet(Element):
    def __init__(self, element):
        self.plurals = set(['Relevance'])
        self.loadxmldata(element)



besfile = File.fromfilename('test/test.bes')
# besfile.printBES()
for fixlet in besfile.fixlets:
    print fixlet.tag
    print fixlet.children['Title'].text
    print fixlet.children['DefaultAction'].hasattribute('id')
    print fixlet.haselement('Relevance')
    for relevance in fixlet.children['Relevance']:
        print relevance.text[0:20]

