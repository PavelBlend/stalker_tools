from . import xray_utils
from .xray_utils import unpack_data as u
from .format_object import ObjectFormat


def parse_friction(d):
    (friction, ), p = u('f', d, 0)


def parse_break_params(d):
    (breakForce, breakTorque), p = u('ff', d, 0)


def parse_ik_flags(d):
    (ik_flags, ), p = u('I', d, 0)


def parse_mass_params(d):
    (mass, ), p = u('f', d, 0)
    massCenter, p = u('fff', d, p)


def parse_ik_joint(d):
    (jointType, ), p = u('I', d, 0)
    for i in range(3):
        Range, p = u('ff', d, p)
        (springFactor0, ), p = u('f', d, p)
        (dampingFactor0, ), p = u('f', d, p)
    (springFactor1, ), p = u('f', d, p)
    (dampingFactor1, ), p = u('f', d, p)


def parse_shape(d):
    shapeTypeNames = {0 : 'undefined', 1 : 'box', 2 : 'sphere', 3 : 'cylinder' }
    (shapeType, ), p = u('H', d, 0)
    shapeTypeName = shapeTypeNames[shapeType]
    (flags, ), p = u('H', d, p)
    rotate, p = u('9f', d, p)
    translate, p = u('3f', d, p)
    halfsize, p = u('3f', d, p)
    sphereCenter, p = u('3f', d, p)
    (sphereRadius, ), p = u('f', d, p)
    cylinderCenter, p = u('3f', d, p)
    cylinderDirection, p = u('3f', d, p)
    (cylinderHeight, ), p = u('f', d, p)
    (cylinderRadius, ), p = u('f', d, p)


def parse_material(d):
    material, p = xray_utils.parse_string(d, 0)


def parse_bin_pose(d):
    offset, p = u('fff', d, 0)
    rotate, p = u('fff', d, p)
    (bind_length, ), p = u('f', d, p)


def parse_def_1(d):
    name, p = xray_utils.parse_string(d, 0)
    print(name)


def parse_def_0(d):
    name, p = xray_utils.parse_string(d, 0)
    parentName, p = xray_utils.parse_string(d, p)
    vMapName, p = xray_utils.parse_string(d, p)


def parse_version(d):
    (version, ), p = u('H', d, 0)


def parse_bone(d):
    p = 0
    dataSize = len(d)
    defType = 0
    bone = ObjectFormat.Version16.Chunks.Main.Bones.Bone
    while p < dataSize:
        (id, cmpr, size), p = u('HHI', d, p)
        cd = d[p : p + size]    # chunk data
        if id == bone.Version.id:
            parse_version(cd)
        elif id == bone.Def.id:
            if defType == 0:
                parse_def_0(cd)
                defType = 1
            else:
                parse_def_1(cd)
        elif id == bone.BindPose.id:
            parse_bin_pose(cd)
        elif id == bone.Material.id:
            parse_material(cd)
        elif id == bone.Shape.id:
            parse_shape(cd)
        elif id == bone.IkJoint.id:
            parse_ik_joint(cd)
        elif id == bone.MassParams.id:
            parse_mass_params(cd)
        elif id == bone.IkFlags.id:
            parse_ik_flags(cd)
        elif id == bone.BreakParams.id:
            parse_break_params(cd)
        elif id == bone.Friction.id:
            parse_friction(cd)
        else:
            xray_utils.un_blk(id)
        p += size


def parse_bones(d):
    p = 0
    dataSize = len(d)
    while p < dataSize:
        (id, cmpr, size), p = u('HHI', d, p)
        parse_bone(d[p : p + size])
        p += size

