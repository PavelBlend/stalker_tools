import bpy, time


def export_object(object, format, path):
    startTime = time.time()
    file = open(path.encode(encoding='cp1251'), 'wb')
    if format == 'CFORM':
        from . import export_cform
        export_cform.export_main(object, file)
    elif format == 'SOM':
        from . import export_som
        export_som.export_main(object, file)
    elif format == 'HOM':
        from . import export_hom
        export_hom.export_main(object, file)
    elif format == 'DM':
        from . import export_dm
        export_dm.export_main(object, file)
    file.close()
    print('{:.6}s'.format(time.time() - startTime))


def export_objects(exportPath):
    scene = bpy.context.scene
    exportFormat = scene.stalkerExportFormat
    exportObjects = scene.stalkerExportObject
    if bpy.context.selected_objects or exportObjects == 'ALL':
        if exportObjects == 'ACTIVE':
            objectList = [bpy.context.active_object, ]
        elif exportObjects == 'SELECT':
            objectList = bpy.context.selected_objects
        elif exportObjects == 'ALL':
            objectList = scene.objects
        for object in objectList:
            fileName = '{}.{}'.format(object.name, exportFormat.lower())
            print('{: <32}'.format(fileName), end=' ')
            export_object(object, exportFormat, exportPath + fileName)

