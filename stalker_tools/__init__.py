bl_info = {'name':     'S.T.A.L.K.E.R. Tools',
           'author':   'Pavel_Blend',
           'version':  (0, 0, 0),
           'blender':  (2, 7, 1),
           'category': 'Import-Export',
           'location': 'Scene properties',
           'description': 'Import/Export X-Ray Engine mesh',
           'wiki_url': '',
           'tracker_url': '',
           'warning': ''}

import bpy
from bpy.props import *
xray_ext = ('ogf', 'dm', 'cform', 'details', 'hom', 'wallmarks', 'som')
tScn = bpy.types.Scene
tScn.xray_path_import = StringProperty(name='Import Path',
                                       default = 'x:\\import\\blender_import\\',
                                       subtype = 'FILE_PATH')


def stalker_tools_main():
    import os, time
    from . import xray_utils

    start_time = time.time()
    path = bpy.context.scene.xray_path_import
    print('\nRUN BATCH X-RAY IMPORT (DIR: {0})\n'.format(path.upper()))
    for file in os.listdir(path):
        ext = file.split('.')[-1]
        if ext in xray_ext:
            print('{: <32}'.format(file), end=' ')
            xray_utils.import_file(path + file)
    finish_time = time.time()
    print('\ntotal time: {:.6}s'.format(finish_time - start_time))


class Stalker_Scene_Panel_Import(bpy.types.Panel):
    bl_label = 'S.T.A.L.K.E.R. Tools'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        scn = bpy.context.scene
        layout = self.layout
        layout.prop(scn, 'xray_path_import')
        layout.operator('stalker_tools.import_xray_mesh',
                        text='S.T.A.L.K.E.R. IMPORT')


class Stalker_Import(bpy.types.Operator):
    bl_idname = 'stalker_tools.import_xray_mesh'
    bl_label = 'S.T.A.L.K.E.R. IMPORT (X-Ray)'

    def execute(self, context):
        stalker_tools_main()
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()

