from .xray_utils import unpack_data as u
from . import xray_utils


def parse_main(d):
    p, fileSz = 0, len(d)
    materials = {}
    while p < fileSz:
        (id, cmpr, sz), p = u('HHI', d, p)
        if id == 0x0:
            (fmtVer, ), p = u('I', d, p)    # 1154-COP = 0
            if fmtVer != 0:
                xray_utils.un_ver('HOM', fmtVer)
                break
        elif id == 0x1:
            tCnt, verts = sz // 40, []
            for index in range(tCnt):    # s - two sided (0/1)
                (x1, y1, z1, x2, y2, z2, x3, y3, z3, s), p = u('9fI', d, p)
                verts.extend(((x1, z1, y1), (x2, z2, y2), (x3, z3, y3)))
                if materials.get(s):
                    materials[(s, 0.0)].append(index)
                else:
                    materials[(s, 0.0)] = [index]
        else:
            xray_utils.un_blk(id)
    faces = xray_utils.generate_face(len(verts))
    materials = list(materials.items())
    somProp = []
    faceMat = {}
    for n, mat in enumerate(materials):
        somProp.append(mat[0])
        for i in mat[1]:
            faceMat[i] = n
    faceIndices = list(faceMat.keys())
    faceIndices.sort()
    matIdices = []
    for i in faceIndices:
        matIdices.append(faceMat[i])
    materials_names = [i for i in range(len(somProp))]
    meshData = {'verts' : verts}
    meshData['faces'] = faces
    meshData['materials'] = materials_names
    meshData['material_indices'] = matIdices
    meshData['som_property'] = somProp
    return meshData

