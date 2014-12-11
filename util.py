__all__ = ["matrix_to_vec", "AttrPack"]

import pyconspack as cpk

from array import array
from pyconspack import Conspack

def matrix_to_vec(m):
    m = m.transposed()
    return array('f',
                 m[0].to_tuple() +
                 m[1].to_tuple() +
                 m[2].to_tuple() +
                 m[3].to_tuple())

class AttrPack:
    def __init__(self, *data, **kw):
        self.preinit(**kw)

        for d in data:
            for key in d:
                setattr(self, re.sub(r'-',r'_', key.name.lower()), d[key])

        return self.postinit(**kw)

    def preinit(self, **kw): pass
    def postinit(self, **kw): pass

    def encode(self):
        return self.__dict__

def defencode(c, name):
    Conspack.register(c, cpk.intern(name, "consmodel"),
                      c.encode, c)
