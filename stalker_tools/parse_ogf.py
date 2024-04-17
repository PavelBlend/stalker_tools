from . import xray_import, xray_utils
from .xray_utils import unpack_data as u


def parse_main(d):
    fmtVer = get_version(d)
    if fmtVer == 4:
        p, fileSz, parseChild = 0, len(d), False
        while p < fileSz:
            (id, sz), p = u('II', d, p)
            if id == HEADER[0]:
                parse_header(d[p : p + sz])
            elif id == TEXTURE[0]:
                imageName = parse_texture(d[p : p + sz])
            elif id == VERTICES[0]:
                verts, uvs = parse_vertices(d[p : p + sz])
            elif id == INDICES[0]:
                faces = parse_indices(d[p : p + sz])
            elif id == CHILDREN[0]:
                parse_childrens(d[p : p + sz])
                parseChild = True
            else:
                # xray_utils.un_blk(id)
                pass
            p += sz
        if not parseChild:
            meshData = {'verts' : verts}
            meshData['faces'] = faces
            meshData['uvs'] = uvs
            meshData['images'] = imageName
            xray_import.create_mesh(meshData)
    else:
        xray_utils.un_ver('OGF', fmtVer)


def get_version(d):
    p, fileSz = 0, len(d)
    while p < fileSz:
        (id, sz), p = u('II', d, p)
        if id == HEADER[0]:
            (fmtVer, ), p = u('B', d, p)
            return fmtVer


def parse_header(d):
    headerData, p = u('BBH10f', d, 0)
    fmtVer, meshType, shaderID = headerData[0:3]
    bBox = headerData[3:9]
    bSphere = headerData[9:13]


def parse_texture(d):
    image, p = xray_utils.parse_string(d, 0)
    shader, p = xray_utils.parse_string(d, p)
    return image


def parse_vertices(d):
    ((vFmt, vCnt), p), verts, uvs = u('2I', d, 0), [], []
    if vFmt == vf['OLD']:
        for _ in range(vCnt):
            (X, Y, Z, u1, u2, u3, U, V), p = u('8f', d, p)
            verts.append((X, Z, Y))
            uvs.append((U, 1 - V))
    elif vFmt == vf['1L'] or vFmt == 1:
        for _ in range(vCnt):
            (X, Y, Z, nX, nY, nZ, tX, tY, tZ, bX, bY, bZ, U, V, matrix), p = \
            u('14fI', d, p)
            verts.append((X, Z, Y))
            # normal = (nX, nZ, nX)
            # t = (tX, tZ, tY)
            # b = (bX, bZ, bY)
            uvs.append((U, 1 - V))
    elif vFmt == vf['2L'] or vFmt == 2:
        for _ in range(vCnt):
            vData, p = u('2H15f', d, p)
            verts.append((vData[2], vData[4], vData[3]))
            uvs.append((vData[15], 1 - vData[16]))
    return verts, uvs


def parse_indices(d):
    ((iCnt, ), p), faces = u('I', d, 0), []
    for _ in range(iCnt // 3):
        (v1, v2, v3), p = u('3H', d, p)
        faces.append((v1, v3, v2))
    return faces


def parse_swidata(d):
    reserved, p = u('4I', d, 0)
    (swiCnt, ), p = u('I', d, p)
    (offset, tCnt, vCnt), p = u('IHH', d, p)
    return offset // 3


def parse_childrens(d):
    p, blkSz = 0, len(d)
    while p < blkSz:
        (id, sz), p = u('II', d, p)
        meshData = parse_children(d[p : p + sz])
        p += sz
        xray_import.create_mesh(meshData)


def parse_children(d):
    p, offset, blkSz = 0, None, len(d)
    while p < blkSz:
        (id, sz), p = u('II', d, p)
        if id == HEADER[0]:
            parse_header(d[p : p + sz])
        elif id == TEXTURE[0]:
            image = parse_texture(d[p : p + sz])
        elif id == VERTICES[0]:
            verts, uvs = parse_vertices(d[p : p + sz])
        elif id == INDICES[0]:
            faces = parse_indices(d[p : p + sz])
        elif id == SWIDATA[0]:
            offset = parse_swidata(d[p : p + sz])
        else:
            # xray_utils.un_blk(id)
            pass
        p += sz
    if offset:
        faces = faces[offset:]
    meshData = {'verts' : verts}
    meshData['faces'] = faces
    meshData['uvs'] = uvs
    meshData['images'] = image
    return meshData


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
meshTypes = {0  : 'NORMAL',
             1  : 'HIERRARHY',
             2  : 'PROGRESSIVE',
             3  : 'SKELETON_ANIM',
             4  : 'SKELETON_GEOMDEF_PM',
             5  : 'SKELETON_GEOMDEF_ST',
             6  : 'LOD',
             7  : 'TREE_ST',
             8  : 'PARTICLE_EFFECT',
             9  : 'PARTICLE_GROUP',
             10 : 'SKELETON_RIGID',
             11 : 'TREE_PM'}

# vertex formats
vf = {'1L'    : 0x12071980,
      '2L'    : 0x240e3300,
      'NL'    : 0x36154c80,
      'OLD'    : 0x00000112}

