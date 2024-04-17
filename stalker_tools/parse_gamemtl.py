from . import xray_utils
from .xray_utils import unpack_data as u


def read_material(d):
    p, size = 0, len(d)
    while p < size:
        (id, cmpr, sz), p = u('HHI', d, p)
        if id == 0x1000:
            (mtlID, ), p = u('I', d, p)
            name, p = xray_utils.parse_string(d, p)
            return name, mtlID
        else:
            p += sz


def read_materials(d):
    p, size, mtls = 0, len(d), {}
    while p < size:
        (matID, matSz), p = u('II', d, p)
        name, mtlID = read_material(d[p : p + matSz])
        mtls[mtlID] = name
        p += matSz
    return mtls


def parse_main(d):
    p, size = 0, len(d)
    while p < size:
        (id, cmpr, sz), p = u('HHI', d, p)
        if id == 0x1000:
            (mtlsVer, ), p = u('H', d, p)
        elif id == 0x1001:
            (matIndex, pairIndex), p = u('II', d, p)
        elif id == 0x1002:
            mtls = read_materials(d[p : p + sz])
            return mtls
        else:
            p += sz

