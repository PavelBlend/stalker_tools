from stalker_tools import xray_import, xray_utils
from stalker_tools.xray_utils import unpack_data as u


def ogf_data_parse(data):
    data_size = len(data)
    position = 0
    parse_children = False
    while position < data_size:
        position, block_id, block_size = xray_utils.read_block(position, data)
        if block_id == HEADER[0]:
            parse_header(data[position : position + block_size])
        elif block_id == TEXTURE[0]:
            texture_name = parse_texture(data[position : position + block_size])
        elif block_id == VERTICES[0]:
            vertices, uvs = parse_vertices(data[position : position + block_size])
        elif block_id == INDICES[0]:
            triangles = parse_indices(data[position : position + block_size])
        elif block_id == CHILDREN[0]:
            parse_childrens(data[position : position + block_size])
            parse_children = True
        else:
            pass
            # print('! UNKNOWN BLOCK: {0}'.format(hex(block_id)))
        position += block_size

    if not parse_children:
        mesh_data = {}
        mesh_data['vertices'] = vertices
        mesh_data['triangles'] = triangles
        mesh_data['uvs'] = uvs
        mesh_data['materials'] = None
        mesh_data['images'] = texture_name
        mesh_data['material_indices'] = None
        xray_import.crete_mesh(mesh_data)


def parse_header(data):
    position = 0
    header_data, position = u('BBH10f', data, position)
    format_version, mesh_type, shader_id = header_data[0:3]
    bbox = header_data[3:9]
    bsphere = header_data[9:13]


def parse_texture(data):
    position = 0
    texture_name, position = xray_utils.parse_string_nul(data, position)
    shader_name, position = xray_utils.parse_string_nul(data, position)
    return texture_name


def parse_vertices(data):
    position = 0
    (format, vertex_count), position = u('2I', data, position)
    vertices, uvs = [], []

    if format == vertex_format['OLD']:
        for i in range(vertex_count):
            vertex_data, position = u('8f', data, position)
            vertices.append((vertex_data[0], vertex_data[2], vertex_data[1]))
            uvs.append((vertex_data[6], 1 - vertex_data[7]))
    elif format == vertex_format['1L'] or vertex_format == 1:
        for i in range(vertex_count):
            vertex_data, position = u('14fI', data, position)
            vertices.append((vertex_data[0], vertex_data[2], vertex_data[1]))
            # normal = vertex_data[3:6]
            # t = vertex_data[6:9]
            # b = vertex_data[9:12]
            uvs.append((vertex_data[12], 1 - vertex_data[13]))
            # matrix = vertex_data[14]
    elif format == vertex_format['2L'] or vertex_format == 2:
        for i in range(vertex_count):
            vertex_data, position = u('2H15f', data, position)
            vertices.append((vertex_data[2], vertex_data[4], vertex_data[3]))
            uvs.append((vertex_data[15], 1 - vertex_data[16]))
        
    return vertices, uvs


def parse_indices(data):
    position = 0
    indices_count, position = u('I', data, position)
    triangles = []

    for i in range(indices_count // 3):
        triangle, position = u('3H', data, position)
        triangles.append((triangle[0], triangle[2], triangle[1]))

    return triangles


def parse_swidata(data):
    position = 0
    reserved, position = u('4I', data, position)
    swidata_count, position = u('I', data, position)
    swidata, position = u('IHH', data, position)
    offset, num_tris, num_verts = swidata
    return offset//3


def parse_childrens(data):
    position = 0
    
    while position < len(data):
        position, mesh_id, mesh_size = xray_utils.read_block(position, data)
        mesh_data = parse_children(data[position : position + mesh_size])
        position += mesh_size
        xray_import.crete_mesh(mesh_data)


def parse_children(data):
    position = 0
    while position < len(data):
        position, block_id, block_size = xray_utils.read_block(position, data)
        if block_id == HEADER[0]:
            parse_header(data[position : position + block_size])
        elif block_id == TEXTURE[0]:
            texture_name = parse_texture(data[position : position + block_size])
        elif block_id == VERTICES[0]:
            vertices, uvs = parse_vertices(data[position : position + block_size])
        elif block_id == INDICES[0]:
            triangles = parse_indices(data[position : position + block_size])
        elif block_id == SWIDATA[0]:
            offset = parse_swidata(data[position : position + block_size])
        else:
            pass
            # print('! UNKNOWN SUBBLOCK: 0x9-{0}'.format(hex(block_id)))
        position += block_size

    if offset:
        triangles = triangles[offset:]

    mesh_data = {}
    mesh_data['vertices'] = vertices
    mesh_data['triangles'] = triangles
    mesh_data['uvs'] = uvs
    mesh_data['materials'] = None
    mesh_data['images'] = texture_name
    mesh_data['material_indices'] = None
    return mesh_data


# ogf format (chunks/blocks) ID, name
HEADER        = (1, 'HEADER')
TEXTURE       = (2, 'TEXTURE')
VERTICES      = (3, 'VERTICES')
INDICES       = (4, 'INDICES')
P_MAP         = (5, 'P_MAP')
SWIDATA       = (6, 'SWIDATA')
VCONTAINER    = (7, 'VCONTAINER')
ICONTAINER    = (8, 'ICONTAINER')
CHILDREN      = (9, 'CHILDREN')
CHILDREN_L    = (10, 'CHILDREN_L')
LODDEF2       = (11, 'LODDEF2')
TREEDEF2      = (12, 'TREEDEF2')
S_BONE_NAMES  = (13, 'S_BONE_NAMES')
S_MOTIONS     = (14, 'S_MOTIONS')
S_SMPARAMS    = (15, 'S_SMPARAMS')
S_IKDATA      = (16, 'S_IKDATA')
S_USERDATA    = (17, 'S_USERDATA')
S_DESC        = (18, 'S_DESC')
S_MOTION_REFS = (19, 'S_MOTION_REFS')
SWICONTAINER  = (20, 'SWICONTAINER')
GCONTAINER    = (21, 'GCONTAINER')
FASTPATH      = (22, 'FASTPATH')
S_LODS        = (23, 'S_LODS')

# no used
mesh_type_names = {0  : 'MT_NORMAL',
                   1  : 'MT_HIERRARHY',
                   2  : 'MT_PROGRESSIVE',
                   3  : 'MT_SKELETON_ANIM',
                   4  : 'MT_SKELETON_GEOMDEF_PM',
                   5  : 'MT_SKELETON_GEOMDEF_ST',
                   6  : 'MT_LOD',
                   7  : 'MT_TREE_ST',
                   8  : 'MT_PARTICLE_EFFECT',
                   9  : 'MT_PARTICLE_GROUP',
                   10 : 'MT_SKELETON_RIGID',
                   11 : 'MT_TREE_PM'}


vertex_format = {'1L'    : 0x12071980,
                 '2L'    : 0x240e3300,
                 'NL'    : 0x36154c80,
                 'OLD'    : 0x00000112}