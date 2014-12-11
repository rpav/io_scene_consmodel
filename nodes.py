__all__ = ["make_node", "CM_Node"]

import bpy
import bpy.types
import bpy_types

import bmesh
import bmesh.ops

import math
import mathutils
import pyconspack as cpk

from array import array
from pyconspack import Conspack
from mathutils import Matrix

import io_scene_consmodel.consmodel as consmodel
from io_scene_consmodel.util import (matrix_to_vec, AttrPack, defencode)

 # Nodes

class CM_Node(AttrPack):
    def preinit(self, ob=None, **kw):
        if(not ob):
            return

        self.name = ob.name
        self.transform = (hasattr(ob, 'matrix_local') and
                          matrix_to_vec(ob.matrix_local))

        vals = ()
        if(hasattr(ob, 'children')):
            vals = ob.children
        elif(hasattr(ob, 'objects')):
            vals = ob.objects

        if(vals):
            self.children = cpk.Vector()
            for val in vals:
                if(not val.parent or val.parent == ob):
                    self.children.append(make_node(val))

def best_integer_type(i):
    if  (i < 2**8):  return 'B'
    elif(i < 2**16): return 'H'
    else:            return 'I'

def int_array(a):
    return array(best_integer_type(len(a)), a)

class CM_Mesh(CM_Node):
    def preinit(self, ob=None, **kw):
        super().preinit(ob, **kw)
        self.primitive_type = cpk.keyword('triangle')
        self.faces = array('I')
        self.vertices = array('f')
        self.normals = array('f')
        self.materials = cpk.Vector()
        self.face_normals = cpk.Vector()

        if(ob):
            if(ob.data in Cache.MESH_CACHE):
                self.faces, self.normals, self.face_normals, self.vertices, self.materials = Cache.MESH_CACHE[ob.data]
            else:
                bm = bmesh.new()
                bm.from_mesh(ob.data)
                bmesh.ops.triangulate(bm, faces=bm.faces)

                for v in bm.verts:
                    self.vertices.extend(v.co.xyz)
                    self.normals.extend(v.normal)

                for f in bm.faces:
                    self.faces.extend((v.index for v in f.verts))
                    self.normals.extend(f.normal)
                    fni = math.floor(len(self.normals)/3)-1

                    if(f.smooth):
                        self.face_normals.extend((v.index for v in f.verts))
                    else:
                        self.face_normals.extend((fni, fni, fni))

                self.faces = int_array(self.faces)
                self.face_normals = int_array(self.face_normals)

                bm.free()

                for slot in ob.material_slots:
                    if(slot.material in Cache.MAT_CACHE):
                        mat = Cache.MAT_CACHE[slot.material]
                    else:
                        mat = CM_Material(ob=slot.material)

                    self.materials.append(mat)

                Cache.MESH_CACHE[ob.data] = (self.faces, self.normals, self.face_normals, self.vertices, self.materials)

class CM_Camera(CM_Node):
    def preinit(self, ob=None, **kw):
        super().preinit(ob, **kw)

        self.fov = ob.data.angle
        self.clip_near = ob.data.clip_start
        self.clip_far = ob.data.clip_end

        self.aspect = ob.data.sensor_width / ob.data.sensor_height

class CM_LightPoint(CM_Node):
    def preinit(self, ob=None, **kw):
        super().preinit(ob, **kw)

        self.position = array('f', ob.location)
        self.diffuse = array('f', (0, 0, 0))
        self.specular = array('f', (0, 0, 0))

        if(ob.data.use_diffuse):
            self.diffuse = array('f', ob.data.energy * ob.data.color)

        if(ob.data.use_specular):
            self.specular = array('f', ob.data.energy * ob.data.color)

        self.attenuation_constant  = 1.0
        self.attenuation_linear    = 0.0
        self.attenuation_quadratic = 0.0

        if(ob.data.falloff_type == 'CONSTANT'):
            self.attenuation_constant  = ob.data.distance
        elif(ob.data.falloff_type == 'INVERSE_LINEAR'):
            self.attenuation_linear    = 1/ob.data.distance
        elif(ob.data.falloff_type == 'INVERSE_SQUARE'):
            self.attenuation_quadratic = 1/(ob.data.distance**2)
        elif(ob.data.falloff_type == 'LINEAR_QUADRATIC_WEIGHTED'):
            self.attenuation_linear    = 1/(ob.data.linear_attenuation * ob.data.distance)
            self.attenuation_quadratic = 1/((ob.data.quadratic_attenuation * ob.data.distance)**2)

class CM_Material(AttrPack):
    def preinit(self, ob=None, **kw):
        self.name = ""
        self.values = v = dict()

        m = ob
        world = consmodel.Consmodel.SCENE.world

        if(ob):
            self.name = m.name
            v['alpha']   = m.alpha
            v['ambient'] = array('f', world.ambient_color * m.ambient)
            v['diffuse'] = array('f', m.diffuse_color * m.diffuse_intensity)

            # This was taken from the Blinn specular code in shadeoutput.c
            roughness = m.specular_hardness * m.specular_intensity
            if(roughness < 0.00001):
                roughness = 0.0
            elif(roughness < 100.0):
                roughness = math.sqrt(1.0/roughness)
            else:
                roughness = math.sqrt(100.0/roughness)

            v['roughness'] = roughness

            specular = list(m.specular_color * m.specular_alpha)
            v['specular'] = array('f', specular)
            v['specular-ior'] = m.specular_ior

            Cache.MAT_CACHE[ob] = self

 # make_node

class Cache:
    CACHE = dict()
    MESH_CACHE = dict()
    MAT_CACHE = dict()

def make_node(bval):
    if(bval in Cache.CACHE):
        return Cache.CACHE[bval]

    if(isinstance(bval, bpy.types.Scene)):
        ob = CM_Node(ob=bval)
    elif(isinstance(bval, bpy_types.Object)):
        if(bval.type == 'MESH'):
            ob = CM_Mesh(ob=bval)
        elif(bval.type == 'CAMERA'):
            ob = CM_Camera(ob=bval)
        elif(bval.type == 'LAMP' and bval.data.type == 'POINT'):
            ob = CM_LightPoint(ob=bval)
        else:
            ob = CM_Node(ob=bval)

    Cache.CACHE[bval] = ob
    return ob

def clear_cache():
    Cache.CACHE = dict()
    Cache.MESH_CACHE = dict()
    Cache.MAT_CACHE = dict()

 # Conspack regs

defencode(CM_Node, "node")
defencode(CM_Mesh, "mesh")
defencode(CM_Camera, "camera")
defencode(CM_LightPoint, "light-point")
defencode(CM_Material, "material-simple")
