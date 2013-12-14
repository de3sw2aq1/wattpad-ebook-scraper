# Copyright (c) 2012, Bin Tan
# This file is distributed under the BSD Licence. See python-epub-builder-license.txt for details.

from epubbuilder import epubbuilder
from genshi.template import TemplateLoader
import os

TEMPLATE_PATH = os.path.join(os.path.split(__file__)[0], "templates")

class Section:

    def __init__(self):
        self.title = ''
        self.subsections = []
        self.css = ''
        self.text = []
        self.templateFileName = 'ez-section.html'

class Book:

    def __init__(self):
        self.impl = epubbuilder.EpubBook()

        self.loader = TemplateLoader(TEMPLATE_PATH)
        self.impl.loader = self.loader

        self.title = ''
        self.authors = []
        self.cover = ''
        self.lang = 'en-US'
        self.sections = []

    def __add_section(self, section, id, depth):
        if depth > 0:
            stream = self.loader.load(section.templateFileName).generate(section = section)
            html = stream.render('xhtml', doctype = 'xhtml11', drop_xml_decl = False)
            item = self.impl.add_html('%s.html' % id, html.decode('utf8'))
            self.impl.add_spine_item(item)
            self.impl.add_toc_map_node(item.dest_path, section.title, parent=None)
            id += '.'
        if len(section.subsections) > 0:
            for i, subsection in enumerate(section.subsections):
                self.__add_section(subsection, id + str(i + 1), depth + 1)

    def make(self, output):
        self.impl.set_title(self.title)
        self.impl.set_language(self.lang)
        for author in self.authors:
            self.impl.add_creator(author)
        if self.cover:
            self.impl.add_cover(self.cover)
        self.impl.add_title_page()
        self.impl.add_toc_page()
        root = Section()
        root.subsections = self.sections
        self.__add_section(root, 's', 0)
        self.impl.create_book(output)
        # self.impl.create_archive(outputDir, outputFile)
        #self.impl.checkEpub('epubcheck-3.0-RC-1.jar', outputFile)

