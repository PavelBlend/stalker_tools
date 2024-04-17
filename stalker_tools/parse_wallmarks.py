from . import xray_utils, xray_import
from .xray_utils import unpack_data as u


def parse_main(d):
    (id, sz, wmCnt), _p = u('III', d, 0)
    for i in range(wmCnt):
        (setCnt, ), _p = u('I', d, _p)
        shader, _p = xray_utils.parse_string(d, _p)
        image, _p = xray_utils.parse_string(d, _p)
        for ii in range(setCnt):
            (bX, bY, bZ, bR, vCnt), _p = u('4fI', d, _p)
            verts, uvs = [], []
            for iii in range(vCnt):
                (X, Y, Z, clr, U, V), _p = u('3fI2f', d, _p)
                verts.append((X, Z, Y))
                uvs.append((U, 1 - V))
            faces = xray_utils.generate_face(len(verts))
            meshData = {'verts' : verts}
            meshData['faces'] = faces
            meshData['uvs'] = uvs
            meshData['images'] = image
            xray_import.create_mesh(meshData)

