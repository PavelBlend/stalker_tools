from struct import pack as p


def export_main(object, file):
    mesh = object.data
    file.write(p('III', 0x0, 4, 0))    # version block
    file.write(p('II', 0x1, len(mesh.polygons) * 44))    # polygons block
    for polygon in mesh.polygons:
        v1x, v1y, v1z = mesh.vertices[polygon.vertices[0]].co.xzy
        v2x, v2y, v2z = mesh.vertices[polygon.vertices[2]].co.xzy
        v3x, v3y, v3z = mesh.vertices[polygon.vertices[1]].co.xzy
        mat = object.material_slots[polygon.material_index].material
        file.write(p('9fIf', v1x, v1y, v1z,
                             v2x, v2y, v2z,
                             v3x, v3y, v3z,
                             mat.stalker2sided,
                             mat.stalkerOCC))

