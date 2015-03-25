# Setup praw
import pip
import imp

def install(package):
    pip.main(['install', package])

# Example
if __name__ == '__main__':
    try:
        imp.find_module('praw')
    except ImportError:
        install('praw')
