"""
Test helper functions.
"""

def visit_all(pages):
    """
    Visit each page object in `pages` (an iterable).
    """
    for page in pages:
        print "Visiting: {}".format(page)
        page.visit()
