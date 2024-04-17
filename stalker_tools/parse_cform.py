from .xray_utils import unpack_data as u
from . import xray_utils
import struct


def parse_level_cform(d):
    (fmtVer, ), _p = u('I', d, 0)
    if fmtVer in (2, 3, 4):    # level.cform
        (vCnt, tCnt), _p = u('II', d, _p)
        bBox, _p = u('6f', d, _p)
        verts, faces, mtls, sectors, mtlInds, sectorsId = [], [], [], [], [], []
        for _ in range(vCnt):
            X, Y, Z = struct.unpack('3f', d[_p : _p + 12])
            _p += 12
            verts.append((X, Z, Y))
        if fmtVer == 4:    # 1537-COP
            for _ in range(tCnt):
                v1, v2, v3, mtl, sector = struct.unpack('3I2H', d[_p : _p + 16])
                _p += 16
                mtlId = mtl & 0x3fff
                # unk1 = mtl >> 15
                # unk2 = mtl >> 14 & 1
                faces.append((v1, v3, v2))
                mtlInds.append(mtlId)
                sectors.append(sector)
                if not mtlId in mtls:
                    mtls.append(mtlId)
                if not sector in sectorsId:
                    sectorsId.append(sector)
        elif fmtVer == 2 or fmtVer == 3:    # 1475-1512
            for _ in range(tCnt):
                (v1, v2, v3), _p = u('3I', d, _p)
                faces.append((v1, v3, v2))
                unknow, _p = u('14B', d, _p)
                (sector, ), _p = u('H', d, _p)
                sectors.append(sector)
                (mtlId, ), _p = u('I', d, _p)
                mtlInds.append(mtlId)
                if not mtlId in mtls:
                    mtls.append(mtlId)
                if not sector in sectorsId:
                    sectorsId.append(sector)
        meshData = {'verts' : verts}
        meshData['faces'] = faces
        meshData['materials'] = mtls
        meshData['material_indices'] = mtlInds
        meshData['sectors'] = sectors
        meshData['sectorsId'] = sectorsId
        meshData['options'] = 'LOAD_GAME_MATERIAL'
        return meshData
    else:
        xray_utils.un_ver('CFORM', fmtVer)
        return None

def get_cform_type(d):
    (x, ), _p = u('I', d, 0)
    if x in (2, 3, 4):
        cform_type = 'LEVEL'
    elif x == 0:
        cform_type = 'BUILD'
    else:
        cform_type = 'UNKNOW'
    return cform_type


def parse_main(d):
    cform_type = get_cform_type(d)
    if cform_type == 'LEVEL':    # level.cform
        meshData = parse_level_cform(d)
    elif cform_type == 'BUILD':    # build.cform
        from . import parse_build_cform
        meshData = parse_build_cform.parse_main(d)
    elif cform_type == 'UNKNOW':
        print(' ! UNKNOW CFORM TYPE')
    return meshData

