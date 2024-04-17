from . import xray_utils
from .xray_utils import unpack_data as u


def parse_main(d, fmt='DM'):
    shader, _p = xray_utils.parse_string(d, 0)
    image, _p = xray_utils.parse_string(d, _p)
    (flgs, minS, maxS, vCnt, iCnt), _p = u('IffII', d, _p)
    dm_options = {'NoWaving' : flgs, 'MinScale' : minS, 'MaxScale' : maxS}
    verts, uvs, faces = [], [], []
    if fmt == 'DET':    # level.details files
        for _ in range(vCnt):
            (X, Y, Z, U, V), _p = u('5f', d, _p)
            verts.append((X, Z, Y))
            uvs.append((U, 1 - V))
    elif fmt == 'DM':    # *.dm files
        for _ in range(vCnt):
            (X, Y, Z, U, V), _p = u('5f', d, _p)
            verts.append((X, Z, Y))
            uvs.append((U, V))
    for _ in range(iCnt // 3):
        (v1, v2, v3), _p = u('3H', d, _p)
        faces.append((v1, v3, v2))
    meshData = {'verts' : verts}
    meshData['faces'] = faces
    meshData['uvs'] = uvs
    meshData['images'] = image
    meshData['dm_options'] = dm_options
    return meshData

