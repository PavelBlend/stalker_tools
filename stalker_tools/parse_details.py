from . import xray_import, xray_utils
from .xray_utils import unpack_data as u
from . import parse_dm


def parse_main(d, loadSlots):
    _p, fmtVer, _fileSz = 0, get_version(d), len(d)
    if fmtVer == 2 or fmtVer == 3:
        while _p < _fileSz:
            (_id, _cmpr, _sz), _p = u('HHI', d, _p)
            if _id == 0x0:
                (fmtVer, obCnt, ofX, ofZ, szX, szZ), _p = u('IIiiII', d, _p)
                _p -= 24
            elif _id == 0x1:
                parse_meshes(d[_p : _p + _sz])
            elif _id == 0x2 and loadSlots:
                if fmtVer == 2:    # 1096-1558
                    locY = parse_slots_v2(d[_p : _p + _sz])
                elif fmtVer == 3:    # 1569-COP
                    locY = parse_slots_v3(d[_p : _p + _sz])
            else:
                xray_utils.un_blk(_id)
            _p += _sz
        slotsCoords, _col, _row, _sSz = [], szX - ofX - 0.5, -ofZ - 0.5, 2
        if loadSlots:
            for _slot in range(szX * szZ):
                if _slot % szX != 0:
                    _col += 1
                    slotsCoords.append((_sSz*_col, _sSz*_row, locY[_slot]))
                else:
                    _col += 1 - szX
                    _row += 1
                    slotsCoords.append((_sSz*_col, _sSz*_row, locY[_slot]))
            xray_import.create_mesh({'verts' : slotsCoords})
    else:
        xray_utils.un_ver('DETAILS', fmtVer)


def get_version(d):
    _p, _fileSz = 0, len(d)
    while _p < _fileSz:
        (_id, _cmpr, _sz), _p = u('HHI', d, _p)
        if _id == 0x0:
            (fmtVer, ), _p = u('I', d, _p)
        _p += _sz
    return fmtVer


def parse_meshes(d):
    _p, _blkSz = 0, len(d)
    while _p < _blkSz:
        (_id, _cmpr, _sz), _p = u('HHI', d, _p)
        xray_import.create_mesh(parse_dm.parse_main(d[_p : _p + _sz], 'DET'))
        _p += _sz


def parse_slots_v3(d):
    _p, locY = 0, []
    for _slot in range(len(d) // 16):
        slotData, _p = u('IIHHHH', d, _p)
        y_base = slotData[0] & 0x3ff
        y_height = (slotData[0] >> 12) & 0xff
        # id0 = (slotData[0] >> 20) & 0x3f
        # id1 = (slotData[0] >> 26) & 0x3f
        # id2 = (slotData[1]) & 0x3f
        # id3 = (slotData[1] >> 6) & 0x3f
        # c_dir = (slotData[1] >> 12) & 0xf
        # c_hemi = (slotData[1] >> 16) & 0xf
        # c_r = (slotData[1] >> 20) & 0xf
        # c_g = (slotData[1] >> 24) & 0xf
        # c_b = (slotData[1] >> 28) & 0xf
        Y = y_base * 0.2 + y_height * 0.1
        if Y > 100 or Y == 0:
            Y -= 200
        else:
            Y += 5
        locY.append(Y)
        # for i in range(2, 6):
        #     a0 = (slotData[i] >> 0) & 0xf
        #     a1 = (slotData[i] >> 4) & 0xf
        #     a2 = (slotData[i] >> 8) & 0xf
        #     a3 = (slotData[i] >> 12) & 0xf
    return locY


def parse_slots_v2(d):
    _p, locY = 0, []
    for _slot in range(len(d) // 22):
        (y_base, y_height), _p = u('ff', d, _p)
        if y_base != 0:
            Y = y_height
        else:
            Y = -200
        locY.append(Y)
        # (id0,  ), _p = u('B', d, _p)
        # (clr0, ), _p = u('H', d, _p)
        # (id1,  ), _p = u('B', d, _p)
        # (clr1, ), _p = u('H', d, _p)
        # (id2,  ), _p = u('B', d, _p)
        # (clr2, ), _p = u('H', d, _p)
        # (id3,  ), _p = u('B', d, _p)
        # (clr3, ), _p = u('H', d, _p)
        # (unk,  ), _p = u('H', d, _p)
        _p += 14
    return locY

