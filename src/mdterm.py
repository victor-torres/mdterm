#coding: utf-8
import os
import sys
from colored import fg, attr
from markdown2 import Markdown
from HTMLParser import HTMLParser

DEFAULT_THEME = ('215', '172', '166', '160', '88', '52')

class Terminal(object):
    """Retrieves terminal rows and columns numbers."""
    def __init__(self):
        # It will only work in unix-based systems
        rows, columns = os.popen('stty size', 'r').read().split()
        self.rows, self.columns = (int(rows), int(columns))

class MarkdownParser(HTMLParser):
    """mdterm - prints markdown in your terminal"""

    def __init__(self, file):
        # Executes HTMLParser init method as it's an 'old-style' class
        HTMLParser.__init__(self)

        self.raw = ''
        self.html = ''
        self.term = ''

        self.theme = DEFAULT_THEME
        self.terminal = Terminal()
        self.list_level = -1
        self.list_level_map = [[0, None] for level in range(1, 7)]

        self.read_file(file)
        self.parse_markdown()
        self.parse_html()

    def read_file(self, file):
        """Reads markdown file and stores its raw data."""
        self.raw = file.read()

    def parse_markdown(self):
        """Parses Markdown into HTML."""
        markdowner = Markdown()
        self.html = markdowner.convert(self.raw)

    def parse_html(self):
        """Parses HTML into Terminal text."""
        self.feed(self.html)

    def handle_starttag(self, tag, attrs):
        """Encountered a start tag"""
        # self.term += '<%s>' % tag
        if tag in ('h%d' % level for level in range(1, 7)):
            # Header [1...6]
            level = int(tag[1]) - 1
            self.term += fg(self.theme[level])
            self.term += ' ' * level

        if tag == 'hr':
            # Ruler
            self.term += '\r%s' % ('-' * self.terminal.columns)

        if tag in ('ul', 'ol') and self.list_level < 6:
            self.list_level += 1
            self.list_level_map[self.list_level][1] = tag

        if tag == 'li':
            self.term += fg(self.theme[self.list_level])
            self.term += ' ' * self.list_level

            if self.list_level_map[self.list_level][1] == 'ol':
                self.list_level_map[self.list_level][0] += 1
                self.term += '%d. ' % self.list_level_map[self.list_level][0]
            else:
                self.term += '- '

            self.term += attr('reset')


    def handle_endtag(self, tag):
        """Encountered an end tag"""
        self.term += attr('reset')

        if tag in ('ul', 'ol'):
            self.list_level_map[self.list_level][0] = 0
            self.list_level -= 1

    def handle_data(self, data):
        """Encountered some data"""
        self.term += data


def main(argv):
    # Verifies if argument number is correct
    if len(argv) != 1:
        print 'Usage: mdterm file...'
        return

    # Tries to open given file
    try:
        markdown_file = open(argv[0])
    except:
        print 'Could not open file.'
        return

    markdown_parser = MarkdownParser(markdown_file)
    print markdown_parser.term
    markdown_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])
