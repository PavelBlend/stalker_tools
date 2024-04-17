from . import xray_utils
from .xray_utils import unpack_data as u
from mathutils import Vector


def parse_main(d):
    (id, cmpr, sz), p = u('HHI', d, 0)
    if id == 0x7777:
        verts, faces, materials, materialIndices = parse_object(d[p : p + sz])
        meshData = {'verts' : verts}
        meshData['faces'] = faces
        meshData['materials'] = materials
        meshData['material_indices'] = materialIndices
        return meshData
    else:
        xray_utils.un_blk(id)


def parse_object(d):
    p, mainSz = 0, len(d)
    while p < mainSz:
        (id, sz), p = u('II', d, p)
        if id == 0x0900:
            (fmtVer, ), p = u('H', d, p)
            if fmtVer != 16:
                xray_utils.un_ver('OBJECT', fmtVer)
                break
        elif id == 0x0903:
            (flags, ), p = u('I', d, p)
        elif id == 0x0907:
            materials = parse_materials(d[p : p + sz])
            p += sz
        elif id == 0x0910:
            verts, faces, materialIndices = parse_meshes(d[p : p + sz])
            p += sz
        elif id == 0x0912:
            userData, p = xray_utils.parse_string(d, p)
        elif id == 0x0921:
            from . import parse_object_bones
            parse_object_bones.parse_bones(d[p : p + sz])
            p += sz
        elif id == 0x0922:
            author, p = xray_utils.parse_string(d, p)
            createDate, p = xray_utils.parse_date(d, p)
            modifer, p = xray_utils.parse_string(d, p)
            editDate, p = xray_utils.parse_date(d, p)
        elif id == 0x0925:
            lodReference, p = xray_utils.parse_string(d, p)
        else:
            xray_utils.un_blk(id)
            p += sz
    return verts, faces, materials, materialIndices


def parse_materials(d):
    ((matCnt, ), p), materials = u('I', d, 0), []
    for i in range(matCnt):
        matName, p = xray_utils.parse_string(d, p)
        engine, p = xray_utils.parse_string(d, p)
        compiler, p = xray_utils.parse_string(d, p)
        material, p = xray_utils.parse_string(d, p)
        image, p = xray_utils.parse_string(d, p)
        uvMapName, p = xray_utils.parse_string(d, p)
        (flags, fvf, tc), p = u('III', d, p)
        materials.append(matName)
    materials = list(range(len(materials)))
    return materials


def parse_meshes(d):
    p, blkSz = 0, len(d)
    while p < blkSz:
        (id, sz), p = u('II', d, p)
        verts, faces, materialIndices = parse_mesh(d[p : p + sz])
        p += sz
    return verts, faces, materialIndices


def parse_mesh(d):
    p, blkSz = 0, len(d)
    while p < blkSz:
        (id, sz), p = u('II', d, p)
        if id == 0x1000:
            (meshVer, ), p = u('H', d, p)
        elif id == 0x1001:
            meshName, p = xray_utils.parse_string(d, p)
        elif id == 0x1002:
            (flags, ), p = u('B', d, p)
        elif id == 0x1004:
            bBox, p = u('6f', d, p)
        elif id == 0x1005:
            ((vCnt, ), p), verts = u('I', d, p), []
            for i in range(vCnt):
                (X, Y, Z), p = u('3f', d, p)
                verts.append((X, Z, Y))
            if sz > vCnt * 12 + 4:    # unknow data (balon_01.object)
                p += sz - vCnt * 12 - 4
        elif id == 0x1006:
            ((tCnt, ), p), faces = u('I', d, p), []
            for i in range(tCnt):
                (v1, uv1, v2, uv2, v3, uv3), p = u('6I', d, p)
                faces.append((v1, v3, v2))
        elif id == 0x1008:
            parse_uv_indices(d[p : p + sz])
            p += sz
        elif id == 0x1009:
            materialIndices = parse_material_indices(d[p : p + sz])
            p += sz
        elif id == 0x1010:
            (option0, option1), p = u('II', d, p)
        elif id == 0x1012:
            parse_uvs(d[p : p + sz])
            p += sz
        elif id == 0x1013:
            smthGrps, p = u('%dI' % (len(d[p : p + sz]) // 4), d, p)
        else:
            xray_utils.un_blk(id)
            p += sz
    return verts, faces, materialIndices


def parse_uv_indices(d):
    (count, ), p = u('I', d, 0)
    for i in range(count):
        (set, ), p = u('B', d, p)
        vmap, p = u('4B', d, p)
        (uv_index, ), p = u('I', d, p)


def parse_material_indices(d):
    ((matCnt, ), p), faceIndices = u('H', d, 0), []
    for matIndex in range(matCnt):
        matName, p = xray_utils.parse_string(d, p)
        (tCnt, ), p = u('I', d, p)
        for i in range(tCnt):
            (faceIndex, ), p = u('I', d, p)
            faceIndices.append((faceIndex, matIndex))
    faceIndices.sort()
    matIndices = []
    for i in faceIndices:
        matIndices.append(i[1])
    return matIndices


def parse_uvs(data):
    (count, ), p = u('I', data, 0)
    for _ in range(count):
        n, p = xray_utils.parse_string(data, p)
        (dim, ), p = u('B', data, p)
        (discon, ), p = u('B', data, p)
        (typ, ), p = u('B', data, p)
        typ = typ & 0x3
        (sz, ), p = u('I', data, p)
        if typ == 0:
            uvs = []
            vtx = []
            for i in range(sz):
                uvs_cur, p = u('ff', data, p)
                uvs.append(uvs_cur)
                (vtx_cur, ), p = u('I', data, p)
                vtx.append(vtx_cur)
            if discon:
                fcs = []
                for i in range(sz):
                    (fcs_cur, ), p = u('I', data, p)
                    fcs.append(fcs_cur)

