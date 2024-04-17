from struct import pack as p
import bpy


def export_main(object, file):
    file.write(b'effects\\rain\x00')
    image = object.material_slots[0].material.texture_slots[0].texture.image.filepath
    texturePath = bpy.context.scene.stalkerTexturesDir
    ext = '.dds'
    texture = bytes(image[len(texturePath) : -len(ext)], encoding='cp1251')
    file.write(p('{}s'.format(len(texture) + 1), texture + b'\x00'))
    options = p('I', int(object.stalkerNoWaving))
    file.write(options)
    file.write(p('ff', object.stalkerMinScale, object.stalkerMaxScale))
    vCnt = len(object.data.vertices)
    tCnt = len(object.data.polygons)
    file.write(p('II', vCnt, tCnt * 3))
    
    vertices = {}
    currentUV = 0
    for face in object.data.polygons:
        for vertex in face.vertices:
            if vertex not in vertices:
                vertices[vertex] = [object.data.vertices[vertex].co[0],
                                    object.data.vertices[vertex].co[1],
                                    object.data.vertices[vertex].co[2],
                                    object.data.uv_layers[0].data[currentUV].uv[0],
                                    object.data.uv_layers[0].data[currentUV].uv[1]]
            currentUV += 1
    x = 0
    for i in range(vCnt):
        file.write(p('fff', vertices[x][0], vertices[x][2], vertices[x][1]))
        file.write(p('ff', vertices[x][3], vertices[x][4]))
        x += 1

    for i in object.data.polygons:
        file.write(p('HHH', i.vertices[0], i.vertices[2], i.vertices[1]))

