import sys
from contextlib import contextmanager

@contextmanager
def open_io(filename=None):
    if filename and filename != '-':
        file_handler = open(filename, 'w+')
    else:
        file_handler = sys.stdout

    try:
        yield file_handler
    finally:
        if file_handler is not sys.stdout:
            file_handler.close()
