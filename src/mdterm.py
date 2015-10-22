#coding: utf-8
import sys
from colored import fg, attr
from markdown2 import Markdown
from HTMLParser import HTMLParser

DEFAULT_THEME = dict(
    headers=dict(
        h1='215',
        h2='172',
        h3='166',
        h4='160',
        h5='88',
        h6='52'
    )
)

class MarkdownParser(HTMLParser):
    """mdterm - prints markdown in your terminal"""

    def __init__(self, file):
        # Executes HTMLParser init method as it's an 'old-style' class
        HTMLParser.__init__(self)

        self.raw = ''
        self.html = ''
        self.term = ''

        self.theme = DEFAULT_THEME

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
        # self.term += tag
        if tag.startswith('h') and tag[1] != 'r':
            self.term += fg(self.theme['headers']['h%s' % tag[1]])
            self.term += ' ' * (int(tag[1]) - 1)

    def handle_endtag(self, tag):
        """Encountered an end tag"""
        # self.term += tag
        if tag.startswith('h'):
            self.term += attr('reset')

    def handle_data(self, data):
        """Encountered some data"""
        self.term += data


def main(argv):
    # Verifies if argument number is correct
    if len(argv) != 1:
        print 'Usage: mdterm file...'
        return

    # Tries to open and read file
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
