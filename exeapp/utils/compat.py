"""
Compatiblity utils for python2/3 shared base. Thx to Armin for this post
http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/
"""


def with_metaclass(meta, *bases):
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
