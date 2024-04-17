from stalker_tools.xray_utils import unpack_data as u


def parse_cform(s):
    I, H, B, f, p, verts, faces = 'I', 'H', 'B', 'f', 0, [], []
    version, p = u(I, s, p)
    vertex_count, p = u(I, s, p)
    face_count, p = u(I, s, p)
    bbox_diagonal, p = u(6*f, s, p)
    
    for i in range(vertex_count):
        vertex, p = u(3*f, s, p)
        verts.append((vertex[0], vertex[2], vertex[1]))
    
    material_indices = []
    materials = {}
    for i in range(face_count):
        face, p = u(3*I, s, p)
        '''
        material_id       = face_data & 0x3fff
        suppress_shadows  = face_data & 0x4000
        suppress_wallmark = face_data & 0x8000
        sector_id         = face_data >> 16 & 0xffff
        '''
        material_id, p = u(B, s, p)
        flags, p = u(B, s, p)
        sector_id, p = u(H, s, p)
        faces.append((face[0], face[2], face[1]))
        material_indices.append(material_id)
        materials[material_id] = True
    materials = list(materials.keys())

    mesh_data = {}
    mesh_data['vertices'] = verts
    mesh_data['triangles'] = faces
    mesh_data['uvs'] = None
    mesh_data['materials'] = materials
    mesh_data['images'] = None
    mesh_data['material_indices'] = material_indices
    return mesh_data

