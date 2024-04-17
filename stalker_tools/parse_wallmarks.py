from stalker_tools import xray_utils, xray_import
from stalker_tools.xray_utils import unpack_data as u
I, H, B, f = 'I', 'H', 'B', 'f'


def parse_main(s):
    p = 0
    block_id, p = u(I, s, p)
    block_size, p = u(I, s, p)
    wallmarks_count, p = u(I, s, p)
    
    for i in range(wallmarks_count):
        set_count, p = u(I, s, p)
        shader, p = xray_utils.parse_string_nul(s, p)
        texture, p = xray_utils.parse_string_nul(s, p)
        for i in range(set_count):
            bounds, p = u(f*4, s, p)
            vertex_count, p = u(I, s, p)
            vertices = []
            uvs = []
            for i in range(vertex_count):
                vertex, p = u(f*3+I+f*2, s, p)
                vertices.append((vertex[0], vertex[2], vertex[1]))
                uvs.append((vertex[4], 1 - vertex[5]))
            # generate faces
            triangles = []
            index = 0
            for i in range(vertex_count//3):
                triangles.append((index, index+2, index+1))
                index += 3

            mesh_data = {}
            mesh_data['vertices'] = vertices
            mesh_data['triangles'] = triangles
            mesh_data['uvs'] = uvs
            mesh_data['images'] = texture
            mesh_data['materials'] = None
            mesh_data['material_indices'] = None
            xray_import.crete_mesh(mesh_data)

