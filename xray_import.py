import bpy, random


def random_material_color(object):
    for material_slot in object.material_slots:
        material = material_slot.material
        red, green, blue = random.random(), random.random(), random.random()
        material.diffuse_color = (red, green, blue)


def assign_materials(object, material_indices):
    for n, material in enumerate(material_indices):
        index = int(object.material_slots[str(material)].path_from_id()[-2])
        object.data.polygons[n].material_index = index


def create_materials(mesh, materials, som_property):
    for n, i in enumerate(materials):
        material = bpy.data.materials.new(str(i))
        mesh.materials.append(material)
        if som_property:
            material.xray_2_sided = som_property[n][0]
            material.xray_occ = som_property[n][1]


def create_uvs(mesh, uvs):
    mesh.uv_textures.new()
    uv_layer = mesh.uv_layers.active.data
    for tris in mesh.polygons:
        for loop_index in range(tris.loop_start, tris.loop_start + tris.loop_total):
            vertex_index = mesh.loops[loop_index].vertex_index
            uv_layer[loop_index].uv = (uvs[vertex_index])


def create_textre(object, image_name, path='T:\\', ext='dds'):
    material = bpy.data.materials.new(image_name + '_Mat')
    bpy.context.scene.objects.active = object
    bpy.ops.object.material_slot_add()
    object.material_slots[0].material = material
    material.specular_intensity = 0
    image = bpy.data.images.load(path + image_name + '.' + ext)
    texture = bpy.data.textures.new(image_name + '_Tex', type = 'IMAGE')
    texture.image = image
    tex_slot = object.material_slots[0].material.texture_slots.add()
    tex_slot.texture = texture
    tex_slot.texture_coords = 'UV'
    
    for i in object.data.uv_textures[0].data:
        i.image = image


def create_object(name='xray_object'):
    mesh = bpy.data.meshes.new(name + '_mesh')
    object = bpy.data.objects.new(name, mesh)
    scene = bpy.context.scene
    scene.objects.link(object)
    return object, mesh


def crete_mesh(mesh_data):
    vertices = mesh_data['vertices']
    triangles = mesh_data['triangles']
    materials = mesh_data['materials']
    material_indices = mesh_data['material_indices']
    uvs = mesh_data['uvs']
    images = mesh_data['images']
    if mesh_data.get('som_property'):
        som_property = mesh_data['som_property']
    else:
        som_property = None
    
    object, mesh = create_object()
    mesh.from_pydata(vertices, (), triangles)
    if materials:
        create_materials(mesh, materials, som_property)
        random_material_color(object)
    if material_indices:
        assign_materials(object, material_indices)
    if uvs:
        create_uvs(mesh, uvs)
    if images:
        create_textre(object, images)

