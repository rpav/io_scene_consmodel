bl_info = {
    "name": "CONSMODEL format",
    "author": "Ryan Pavlik",
    "version": (1, 0, 0),
    "blender": (2, 70, 0),
    "location": "File > Import-Export",
    "description": "Export CONSMODEL",
    "warning": "",
    "wiki_url": "",
    "support": "COMMUNITY",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    if("export_cmdl" in locals()):
        print("Reloading export_cmdl")
        imp.reload(export_cmdl)

import bpy
from bpy.props import (StringProperty)
from bpy_extras.io_utils import (ImportHelper)

class ExportCMDL(bpy.types.Operator, ImportHelper):
    bl_idname = "export_scene.cmdl"
    bl_label = "Export CMDL"

    filename_ext = '.cmdl'
    filter_glob = StringProperty(
        default='*.cmdl',
        options={'HIDDEN'}
        )

    def execute(self, context):
        from io_scene_consmodel import export_cmdl

        kw = self.as_keywords()
        export_cmdl.save(self, context, **kw)

        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(ExportCMDL.bl_idname, text="CONSMODEL (.cmdl)")

def register():
    bpy.utils.register_module(__name__)
    #bpy.types.INFO_MT_file_export.append(menu_func_export)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    #bpy.types.INFO_MT_file_export.remove(menu_func_export)
 
if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
    
