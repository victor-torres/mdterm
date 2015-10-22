#coding: utf-8
import sys
from markdown2 import Markdown

class MarkdownParser(object):
    """mdterm - prints markdown in your terminal"""

    def __init__(self, file):
        # Reads file and store its raw data
        markdowner = Markdown()
        self.raw = file.read()
        self.html = markdowner.convert(self.raw)


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
    print markdown_parser.html

if __name__ == "__main__":
    main(sys.argv[1:])
