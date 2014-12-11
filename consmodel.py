import bpy
import bpy_types

import pyconspack as cpk
from pyconspack import Conspack

import io_scene_consmodel.nodes
from io_scene_consmodel.util import (AttrPack, defencode)

class Consmodel(AttrPack):
    SCENE = None

    def preinit(self, **kw):
        self.stagings = cpk.Vector()

    def postinit(self, scenes=(), **kw):
        for scene in scenes:
            Consmodel.SCENE = scene
            self.stagings.append(io_scene_consmodel.nodes.make_node(scene))

        Consmodel.SCENE = None
            
 # Conspack regs

defencode(Consmodel, "model")
