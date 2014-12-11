import bpy

import pyconspack as cpk
from pyconspack import Conspack

import io_scene_consmodel.nodes
from io_scene_consmodel.consmodel import Consmodel

def save(self, context, **kw):
    with open(kw['filepath'], 'wb') as f:
        io_scene_consmodel.nodes.clear_cache()
        ba = Conspack.encode(Consmodel(scenes=bpy.data.scenes),
                             sub_underscores=True,
                             all_floats_single=True)
        f.write(Conspack.encode(["CMDL", 1, 0, 0]))
        f.write(ba)
        io_scene_consmodel.nodes.clear_cache()
