from .xray_utils import unpack_data as u


def parse_0x1(d):
    p = 0
    dataSize = len(d)
    mtlInds, mtls, sectors, sectorsId = [], [], [], []
    while p < dataSize:
        (sector, mtlId, u2, u3, u4, u5, u6, u7, u8), p = u('II6fI', d, p)
        mtlInds.append(mtlId)
        sectors.append(sector)
        if not mtlId in mtls:
            mtls.append(mtlId)
        if not sector in sectorsId:
            sectorsId.append(sector)
    global meshData
    meshData['materials'] = mtls
    meshData['material_indices'] = mtlInds
    meshData['sectors'] = sectors
    meshData['sectorsId'] = sectorsId
    meshData['options'] = 'LOAD_GAME_MATERIAL'


def parse_mesh(d):
    (fmtVer, vCnt, tCnt), p = u('III', d, 0)
    bbox, p = u('6f', d, p)
    verts, faces = [], []
    for i in range(vCnt):
        (x, y, z), p  = u('fff', d, p)
        verts.append((x, z, y))
    for i in range(tCnt):
        (v1, v2, v3, unknow), p = u('4I', d, p)
        faces.append((v1, v3, v2))
    global meshData
    meshData['verts'] = verts
    meshData['faces'] = faces
    return meshData


def parse_main(d):
    p = 0
    dataSize = len(d)
    while p < dataSize:
        (id, cmpr, sz), p = u('HHI', d, p)
        cd = d[p : p + sz]
        if id == 0x0:
            parse_mesh(cd)
        elif id == 0x1:
            parse_0x1(cd)
        p += sz
    global meshData
    return meshData


meshData = {}

