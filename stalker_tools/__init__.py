bl_info = {'name'        : 'S.T.A.L.K.E.R. Tools',
           'author'      : 'Pavel_Blend',
           'version'     : (0, 0, 1),    # 05.07.2015 14:28
           'blender'     : (2, 7, 1),
           'category'    : 'Import-Export',
           'location'    : 'Properties > Scene | Object | Material',
           'support'     : 'COMMUNITY',
           'description' : 'Import X-Ray Engine mesh'}


import bpy, os, time
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty)
from . import xray_import


def load_desc(ext):
    return 'Load *.{} files'.format(ext)


def save_desc(ext):
    return 'Export select objects to *.{}'.format(ext)


def bool_prop(ext):
    return BoolProperty(name=ext,
                        description=load_desc(ext),
                        default=True)


importPath = 'X:\\import\\blender_import\\'
exportPath = 'X:\\import\\blender_export\\'
texturesPath = 'T:\\'
gamemtlPath = 'X:\\gamedata\\gamemtl.xr'
typeScn = bpy.types.Scene
typeScn.stalkerImportDir = StringProperty(name='Import Path',
                                          default = importPath,
                                          subtype = 'DIR_PATH')
typeScn.stalkerExportDir = StringProperty(name='Export Path',
                                          default = exportPath,
                                          subtype = 'DIR_PATH')
typeScn.stalkerTexturesDir = StringProperty(name='Textures',
                                            default = texturesPath,
                                            subtype = 'DIR_PATH')
typeScn.stalkerGameMtlDir = StringProperty(name='Game Materials',
                                           default = gamemtlPath,
                                           subtype = 'FILE_PATH')
typeScn.stalkerExportFormat = EnumProperty(items=[
                                        ('CFORM', 'Cform', save_desc('cform')),
                                        ('SOM', 'Som', save_desc('som')),
                                        ('HOM', 'Hom', save_desc('hom')),
                                        ('DM', 'Dm', save_desc('dm'))],
                                        name='Export Format')
typeScn.stalkerExportObject = EnumProperty(items=[
                                          ('ACTIVE', 'Active', ''),
                                          ('SELECT', 'Select', ''),
                                          ('ALL', 'All', '')],
                                          name='Export Objects')
typeScn.stalkerOBJECT = bool_prop('object')
typeScn.stalkerOGF = bool_prop('ogf')
typeScn.stalkerDM = bool_prop('dm')
typeScn.stalkerCFORM = bool_prop('cform')
typeScn.stalkerDETAILS = bool_prop('details')
typeScn.stalkerHOM = bool_prop('hom')
typeScn.stalkerWALLMARKS = bool_prop('wallmarks')
typeScn.stalkerSOM = bool_prop('som')
typeScn.stalkerGEOM = bool_prop('geom')
typeScn.stalkerERR = bool_prop('err')
typeScn.stalkerLoadSlots = BoolProperty(name='Load Slots',
                                        description='',
                                        default=True)

tObj = bpy.types.Object
tObj.stalkerMinScale = FloatProperty(name='Min Scale',
                                     default=1,
                                     min=0.1,
                                     max=100.0,
                                     description = '')
tObj.stalkerMaxScale = FloatProperty(name='Max Scale',
                                     default=1,
                                     min=0.1,
                                     max=100.0,
                                     description = '')
tObj.stalkerNoWaving = BoolProperty(name='No Waving',
                                    description='',
                                    default=True)
tMat = bpy.types.Material
tMat.stalkerShader = StringProperty(name='Shader',
                                    default = 'default')
tMat.stalkerCompile = StringProperty(name='Compile',
                                     default = 'default')
tMat.stalkerGameMtl = StringProperty(name='Game Mtl',
                                     default = 'default')
tMat.stalkerMatID = IntProperty(name='Material ID',
                                description='Material id in gamemtl.xr',
                                default=0,
                                min=0,
                                max=16383)
tMat.stalkerOCC = FloatProperty(name='Sound Occlusion',
                                default=0,
                                min=0,
                                max=1,
                                description = 'X-Ray SDK > Shader Editor > '\
                                'Material > Item Properties > '\
                                'Factors > Sound Occlusion')
tMat.stalker2sided = BoolProperty(name='2 Sided',
                                  description = 'X-Ray SDK > Actor Editor > '\
                                  'Surfaces > Surface > 2 Sided')


class StalkerScenePanel(bpy.types.Panel):
    bl_label = 'S.T.A.L.K.E.R. Tools'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        label = layout.label('Import Formats:')
        row1 = layout.row(align=True)
        row2 = layout.row(align=True)
        row3 = layout.row(align=True)
        row4 = layout.row(align=True)
        row1.prop(scn, 'stalkerCFORM')
        row1.prop(scn, 'stalkerDETAILS')
        row1.prop(scn, 'stalkerDM')
        row2.prop(scn, 'stalkerGEOM')
        row2.prop(scn, 'stalkerHOM')
        row2.prop(scn, 'stalkerOBJECT')
        row3.prop(scn, 'stalkerOGF')
        row3.prop(scn, 'stalkerSOM')
        row3.prop(scn, 'stalkerWALLMARKS')
        row4.prop(scn, 'stalkerERR')
        layout.prop(scn, 'stalkerImportDir')
        layout.prop(scn, 'stalkerExportDir')
        layout.prop(scn, 'stalkerTexturesDir')
        layout.prop(scn, 'stalkerGameMtlDir')
        layout.prop(scn, 'stalkerExportFormat')
        layout.prop(scn, 'stalkerExportObject')
        label = layout.label('Details Options:')
        layout.prop(scn, 'stalkerLoadSlots')
        layout.operator('stalker.batch_import', text='Batch Import')
        layout.operator('stalker.batch_export', text='Batch Export')


class StalkerObjectPanel(bpy.types.Panel):
    bl_label = 'S.T.A.L.K.E.R. Tools'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        layout = self.layout
        label = layout.label('DM options:')
        ob = bpy.context.object
        layout.prop(ob, 'stalkerMinScale')
        layout.prop(ob, 'stalkerMaxScale')
        layout.prop(ob, 'stalkerNoWaving')
        


class StalkerMaterialPanel(bpy.types.Panel):
    bl_label = 'S.T.A.L.K.E.R. Tools'
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @classmethod
    def poll(cls, context):
        return context.material

    def draw(self, context):
        layout = self.layout
        mat = bpy.context.object.active_material
        layout.prop(mat, 'stalkerShader')
        layout.prop(mat, 'stalkerCompile')
        layout.prop(mat, 'stalkerGameMtl')
        layout.prop(mat, 'stalker2sided')
        layout.prop(mat, 'stalkerMatID')
        layout.prop(mat, 'stalkerOCC')


class StalkerImportMesh(bpy.types.Operator):
    bl_idname = 'stalker.batch_import'
    bl_label = 'Stalker Batch Import'

    def execute(self, context):
        startTime = time.time()
        path = context.scene.stalkerImportDir
        print('\nRUN STALKER BATCH IMPORT (DIR: {0})\n'.format(path.upper()))
        scn = context.scene
        xrayExt = []
        if scn.stalkerCFORM:
            xrayExt.append('cform')
        if scn.stalkerDETAILS:
            xrayExt.append('details')
        if scn.stalkerDM:
            xrayExt.append('dm')
        if scn.stalkerERR:
            xrayExt.append('err')
        if scn.stalkerGEOM:
            # xrayExt.append('geom')
            pass
        if scn.stalkerHOM:
            xrayExt.append('hom')
        if scn.stalkerOBJECT:
            xrayExt.append('object')
        if scn.stalkerOGF:
            xrayExt.append('ogf')
        if scn.stalkerSOM:
            xrayExt.append('som')
        if scn.stalkerWALLMARKS:
            xrayExt.append('wallmarks')
        for file in os.listdir(path):
            ext = file.split('.')[-1]
            if ext in xrayExt:
                print('{: <32}'.format(file), end=' ')
                xray_import.import_file(path + file)
        print('\ntotal time: {:.6}s'.format(time.time() - startTime))
        return {'FINISHED'}


class StalkerExportMesh(bpy.types.Operator):
    bl_idname = 'stalker.batch_export'
    bl_label = 'Stalker Batch Export'

    def execute(self, context):
        startTime = time.time()
        from . import xray_export
        path = bpy.context.scene.stalkerExportDir
        print('\nRUN STALKER BATCH EXPORT (DIR: {0})\n'.format(path.upper()))
        xray_export.export_objects(path)
        print('\ntotal time: {:.6}s'.format(time.time() - startTime))
        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()

