from stalker_tools import xray_utils
from stalker_tools.xray_utils import unpack_data as u


def parse_main(d):
    p = 0
    while p < len(d):
        p, block_id, block_size = xray_utils.read_block(p, d)
        if block_id == 0x0:
            format_version, p = u('I', d, p)  # 2205-CoP = 0
        elif block_id == 0x1:
            mesh_data = parse_tris(d[p : p + block_size])
            p += block_size
            return mesh_data


def parse_tris(d):
    p = 0
    tris_count = len(d) // 44
    vertices = []
    options = []
    for i in range(tris_count):
        tris_data, p = u('9fIf', d, p)
        v1_x, v1_y, v1_z = tris_data[0:3]
        v2_x, v2_y, v2_z = tris_data[3:6]
        v3_x, v3_y, v3_z = tris_data[6:9]
        # occ - ShaderEditor>Materials>Property>Factors>SoundOcclusion(0.0-1.0)
        two_sided, occ = tris_data[9:11]
        options.append((i, two_sided, occ))
        vertices.append((v1_x, v1_z, v1_y))
        vertices.append((v2_x, v2_z, v2_y))
        vertices.append((v3_x, v3_z, v3_y))
    # generate triangle indices
    triangles = []
    for index in range(0, len(vertices), 3):
        triangles.append((index, index + 2, index + 1))
    # generate material indices
    materials = {}
    for i in options:
        if materials.get((i[1], i[2])):
            materials[(i[1], i[2])].append(i[0])
        else:
            materials[(i[1], i[2])] = [i[0]]
    materials = list(materials.items())
    tris_indices = {}
    som_property = []
    for n, material in enumerate(materials):
        som_property.append(material[0])
        for tris_index in material[1]:
            tris_indices[tris_index] = n
    tris_indices = list(tris_indices.items())
    tris_indices.sort()
    material_indices = []
    materials_names = [str(i) for i in range(len(materials))]
    for i in tris_indices:
        material_indices.append(i[1])
    mesh_data = {}
    mesh_data['vertices'] = vertices
    mesh_data['triangles'] = triangles
    mesh_data['uvs'] = None
    mesh_data['images'] = None
    mesh_data['materials'] = materials_names
    mesh_data['material_indices'] = material_indices
    mesh_data['som_property'] = som_property
    return mesh_data

