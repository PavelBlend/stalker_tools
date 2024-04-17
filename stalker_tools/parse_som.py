from .xray_utils import unpack_data as u
from . import xray_utils


def parse_main(d):
    _p, _fileSz = 0, len(d)
    while _p < _fileSz:
        (_id, _cmpr, _sz), _p = u('HHI', d, _p)
        if _id == 0x0:
            (fmtVer, ), _p = u('I', d, _p)
            if fmtVer != 0:    # 2205-CoP
                xray_utils.un_ver('SOM', fmtVer)
                break
        elif _id == 0x1:
            meshData = parse_tris(d[_p : _p + _sz])
            _p += _sz
            return meshData
        else:
            xray_utils.un_blk(_id)


def parse_tris(d):
    _p, tCnt, verts, faces, opt = 0, len(d) // 44, [], [], []
    materials = {}
    for _index in range(tCnt):    # s - two sided
        (x1, y1, z1, x2, y2, z2, x3, y3, z3, s, occ), _p = u('9fIf', d, _p)
        verts.extend(((x1, z1, y1), (x2, z2, y2), (x3, z3, y3)))
        if materials.get((s, occ)):
            materials[(s, occ)].append(_index)
        else:
            materials[(s, occ)] = [_index]
    faces = xray_utils.generate_face(len(verts))
    # generate material indices
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

