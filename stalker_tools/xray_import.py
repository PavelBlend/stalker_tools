import bpy, random, time
from . import xray_utils


def random_material_color(object):
    for material_slot in object.material_slots:
        material_slot.material.diffuse_color = (random.random(),
                                                random.random(),
                                                random.random())


def assign_materials(object, material_indices, matSlots):
    for n, material in enumerate(material_indices):
        index = matSlots[material]
        object.data.polygons[n].material_index = index


def create_materials(mesh, materials, som_property, options):
    matSlots = {}
    if options == 'LOAD_GAME_MATERIAL':
        from . import parse_gamemtl
        path = bpy.context.scene.stalkerGameMtlDir
        d = xray_utils.read_file(path)
        if d:
            mtls = parse_gamemtl.parse_main(d)
            for n, i in enumerate(materials):
                material = bpy.data.materials.new(mtls[i])
                mesh.materials.append(material)
                material.stalkerMatID = i
                matSlots[i] = n
    else:
        for n, i in enumerate(materials):
            material = bpy.data.materials.new(str(i))
            mesh.materials.append(material)
            matSlots[i] = n
            if som_property:
                material.stalker2sided = som_property[n][0]
                material.stalkerOCC = som_property[n][1]
    return matSlots


def create_uvs(mesh, uvs):
    mesh.uv_textures.new()
    uv_layer = mesh.uv_layers.active.data
    for tris in mesh.polygons:
        for loop_index in range(tris.loop_start, tris.loop_start + tris.loop_total):
            vertex_index = mesh.loops[loop_index].vertex_index
            uv_layer[loop_index].uv = (uvs[vertex_index])


def create_texture(object, image_name, ext='dds'):
    path = bpy.context.scene.stalkerTexturesDir
    if bpy.data.materials.get(image_name):
        material = bpy.data.materials[image_name]
    else:
        material = bpy.data.materials.new(image_name)
    object.data.materials.append(material)
    material.specular_intensity = 0
    if bpy.data.images.get(image_name + '.' + ext):
        image = bpy.data.images[image_name + '.' + ext]
    else:
        image = bpy.data.images.load(path + image_name + '.' + ext)
    if bpy.data.textures.get(image_name):
        texture = bpy.data.textures[image_name]
    else:
        texture = bpy.data.textures.new(image_name, type = 'IMAGE')
        texture.image = image
    if not object.material_slots[0].material.texture_slots[0]:
        tex_slot = object.material_slots[0].material.texture_slots.add()
        tex_slot.texture = texture
        tex_slot.texture_coords = 'UV'
    for i in object.data.uv_textures[0].data:
        i.image = image


def create_object(name='xray_object'):
    object = bpy.data.objects.new(name, bpy.data.meshes.new(name + '_mesh'))
    bpy.context.scene.objects.link(object)
    return object


def create_sectors(object, sectors, sectorsId):
    bpy.context.scene.objects.active = object
    for i in sectorsId:
        object.vertex_groups.new(name=str(i))
    for i in object.data.polygons:
        sectorID = sectors[i.index]
        for j in i.vertices:
            object.vertex_groups[str(sectorID)].add((j,), 1.0, 'REPLACE')


def assign_dm_option(object, dm_options):
    object.stalkerMinScale = dm_options['MinScale']
    object.stalkerMaxScale = dm_options['MaxScale']
    object.stalkerNoWaving = dm_options['NoWaving']


def create_mesh(meshData):
    if meshData:
        verts = meshData.get('verts')
        edges = meshData.get('edges')
        faces = meshData.get('faces')
        materials = meshData.get('materials')
        material_indices = meshData.get('material_indices')
        uvs = meshData.get('uvs')
        images = meshData.get('images')
        som_property = meshData.get('som_property')
        sectors = meshData.get('sectors')
        sectorsId = meshData.get('sectorsId')
        options = meshData.get('options')
        dm_options = meshData.get('dm_options')
        object = create_object()
        mesh = object.data
        if not faces:
            faces = ()
        if not edges:
            edges = ()
        mesh.from_pydata(verts, edges, faces)
        if materials:
            matSlots = create_materials(mesh, materials, som_property, options)
            random_material_color(object)
        if material_indices:
            assign_materials(object, material_indices, matSlots)
        if uvs:
            create_uvs(mesh, uvs)
        if images:
            create_texture(object, images)
        if sectors and sectorsId:
            create_sectors(object, sectors, sectorsId)
        if dm_options:
            assign_dm_option(object, dm_options)


def parse_file(file_data, ext):
    from . import (parse_cform,
                   parse_details,
                   parse_dm,
                   parse_err,
                   parse_hom,
                   parse_object,
                   parse_ogf,
                   parse_som,
                   parse_wallmarks,)
    meshData = None
    if ext == 'cform':
        meshData = parse_cform.parse_main(file_data)
    elif ext == 'details':
        loadSlots = bpy.context.scene.stalkerLoadSlots
        parse_details.parse_main(file_data, loadSlots)
    elif ext == 'dm':
        meshData = parse_dm.parse_main(file_data)
    elif ext == 'hom':
        meshData = parse_hom.parse_main(file_data)
    elif ext == 'err':
        meshData = parse_err.parse_main(file_data)
    elif ext == 'wallmarks':
        parse_wallmarks.parse_main(file_data)
    elif ext == 'ogf':
        parse_ogf.parse_main(file_data)
    elif ext == 'object':
        meshData = parse_object.parse_main(file_data)
    elif ext == 'som':
        meshData = parse_som.parse_main(file_data)
    return meshData


def import_file(absolute_path):
    startTime = time.time()
    ext = absolute_path.split('.')[-1]
    file_data = xray_utils.read_file(absolute_path)
    if file_data:
        meshData = parse_file(file_data, ext)
        create_mesh(meshData)
    print('{:.6}s'.format(time.time() - startTime))

