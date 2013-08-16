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

class Fixlet:
    def __init__(self, element):
        self.element = element
        for child in element:
            tag = element.tag
            if element.tag == 'Title':

        print "Fixlet initialized: " + element.find('Title').text

    def set_title(self, title):
        self.title = title



reader = File.fromfilename('test/test.bes')
reader.printBES()