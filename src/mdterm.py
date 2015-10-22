#coding: utf-8
import sys
from markdown2 import Markdown
from HTMLParser import HTMLParser

class MarkdownParser(HTMLParser):
    """mdterm - prints markdown in your terminal"""

    def __init__(self, file):
        # Executes HTMLParser init method
        # as it's an 'old-style' class
        HTMLParser.__init__(self)
        # Reads file and store its raw data
        self.raw = file.read()
        # Parses Markdown into HTML
        markdowner = Markdown()
        self.html = markdowner.convert(self.raw)
        # Parses HTML into Terminal text
        self.term = ''
        self.feed(self.html)

    def handle_starttag(self, tag, attrs):
        """Encountered a start tag"""
        # self.term += tag
        pass

    def handle_endtag(self, tag):
        """Encountered an end tag"""
        # self.term += tag
        pass

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

if __name__ == "__main__":
    main(sys.argv[1:])
