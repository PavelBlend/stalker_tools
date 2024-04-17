from .xray_utils import unpack_data as u
from . import xray_utils, xray_import


def parse_main(d):
    p, size = 0, len(d)
    while p < size:
        (id, cmpr, sz), p = u('HHI', d, p)
        if id == 0x0:
            parse_invalid_vertex(d[p : p + sz])
        elif id == 0x1:
            parse_invalid_edge(d[p : p + sz])
        elif id == 0x2:
            parse_zero_area_face(d[p : p + sz])
        else:
            xray_utils.un_blk(id)
        p += sz


def parse_zero_area_face(d):
    (tCnt, ), p = u('I', d, 0)
    verts, faces = [], []
    for _ in range(tCnt):
        (X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3), p = u('9f', d, p)
        verts.extend(((X1, Z1, Y1), (X2, Z2, Y2), (X3, Z3, Y3)))
    for index in range(0, len(verts), 3):
        faces.append((index, index + 2, index + 1))
    if len(faces):
        xray_import.create_mesh({'verts' : verts, 'faces' : faces})


def parse_invalid_edge(d):
    (eCnt, ), p = u('I', d, 0)
    verts, edges = [], []
    for _ in range(eCnt):
        (X1, Y1, Z1, X2, Y2, Z2), p = u('6f', d, p)
        verts.extend(((X1, Z1, Y1), (X2, Z2, Y2)))
    for index in range(0, len(verts), 2):
        edges.append((index, index + 1))
    if len(edges):
        xray_import.create_mesh({'verts' : verts, 'edges' : edges})


def parse_invalid_vertex(d):
    (vCnt, ), p = u('I', d, 0)
    verts = []
    for _ in range(vCnt):
        (X1, Y1, Z1), p = u('3f', d, p)
        verts.append((X1, Z1, Y1))
    if len(verts):
        xray_import.create_mesh({'verts' : verts})

