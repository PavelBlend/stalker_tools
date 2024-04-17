from stalker_tools import xray_utils, xray_import
from stalker_tools.xray_utils import unpack_data as u


def details_data_parse(details_data):
    position = 0
    while position < len(details_data):
        position, block_id, block_size = xray_utils.read_block(position, details_data)
        
        if block_id == 0x0:
            slots_coords = parse_header(details_data[position : position + block_size], coord_y)
            position += block_size
            mesh_data = {}
            mesh_data['vertices'] = slots_coords
            mesh_data['triangles'] = ()
            mesh_data['uvs'] = None
            mesh_data['images'] = None
            mesh_data['material_indices'] = None
            mesh_data['materials'] = None
            xray_import.crete_mesh(mesh_data)
        elif block_id == 0x1:
            parse_meshes(details_data[position : position + block_size])
            position += block_size
        elif block_id == 0x2:
            coord_y = parse_slots(details_data[position : position + block_size])
            position += block_size
        else:
            print(' ! UNKNOW BLOCK ({0}) {1} BYTES'.format(hex(block_id), block_size))
            position += block_size


def parse_header(data, coord_y):
    position = 0
    header_data, position = u('IIiiII', data, position)
    version, object_count, offset_x, offset_z, size_x, size_z = header_data
    slots_coords = []
    slots_count = size_x * size_z
    column = 0 - offset_x + size_x
    row = 1 - offset_z
    
    for slot in range(slots_count):
        if slot % size_x != 1:
            column += 1
            slots_coords.append((2*(column), 2*(row), coord_y[slot]))
        else:
            column += 1 - size_x
            row += 1
            slots_coords.append((2*(column), 2*(row), coord_y[slot]))
    return slots_coords


def parse_meshes(data):
    position = 0
    while position < len(data):
        mesh_info, position = u('2I', data, position)
        mesh_id, mesh_size = mesh_info
        parse_mesh(data[position : position + mesh_size], mesh_id)
        position += mesh_size


def parse_mesh(data, mesh_id):
    position = 0
    shader, position = xray_utils.parse_string_nul(data, position)
    texture, position = xray_utils.parse_string_nul(data, position)
    mesh_info, position = u('IffII', data, position)
    flags, min_scale, max_scale, vertices_count, indices_count = mesh_info
    vertices = []
    uvs = []

    for vertex_id in range(vertices_count):
        vertex_data, position = u('5f', data, position)
        position_x, position_y, position_z, uv_x, uv_y = vertex_data
        vertices.append((position_x, position_z, position_y))
        uvs.append((uv_x, 1 - uv_y))

    triangles = []
    
    for index_id in range(indices_count//3):
        triangle_data, position = u('3H', data, position)
        index_1, index_2, index_3  = triangle_data
        triangles.append((index_1, index_3, index_2))
    
    mesh_data = {}
    mesh_data['vertices'] = vertices
    mesh_data['triangles'] = triangles
    mesh_data['uvs'] = uvs
    mesh_data['images'] = 'details\\build_details'
    mesh_data['material_indices'] = None
    mesh_data['materials'] = None
    
    xray_import.crete_mesh(mesh_data)


def parse_slots(data):
    position = 0
    coord_y = []
    for slot in range(len(data)//16):
        slot_data, position = u('IIHHHH', data, position)
        y_base = slot_data[0] & 0x3ff
        y_height = (slot_data[0] >> 12) & 0xff
        id0 = (slot_data[0] >> 20) & 0x3f
        id1 = (slot_data[0] >> 26) & 0x3f
        id2 = (slot_data[1]) & 0x3f
        id3 = (slot_data[1] >> 6) & 0x3f
        c_dir = (slot_data[1] >> 12) & 0xf
        c_hemi = (slot_data[1] >> 16) & 0xf
        c_r = (slot_data[1] >> 20) & 0xf
        c_g = (slot_data[1] >> 24) & 0xf
        c_b = (slot_data[1] >> 28) & 0xf
        position_y = (y_base*0.2-200)+(y_height*0.1)
        coord_y.append(position_y)

        for i in range(2, 6):
            a0 = (slot_data[i] >> 0) & 0xf
            a1 = (slot_data[i] >> 4) & 0xf
            a2 = (slot_data[i] >> 8) & 0xf
            a3 = (slot_data[i] >> 12) & 0xf

    return coord_y

