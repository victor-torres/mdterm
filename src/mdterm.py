#coding: utf-8
import sys

def main(argv):
    """mdterm - prints markdown in your terminal"""
    # Verifies if argument number is correct
    if len(argv) != 1:
        print 'Usage: mdterm file...'
        return
        
    # Tries to open and read file
    try:
        markdown_file = open(argv[0]).read()
    except:
        print 'Could not open file.'
        return

    # Prints file
    print markdown_file

if __name__ == "__main__":
    main(sys.argv[1:])
