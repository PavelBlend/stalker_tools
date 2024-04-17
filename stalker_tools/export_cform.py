from struct import pack as p


def export_main(object, file):
    fmtVer = 4
    file.write(p('I', fmtVer))
    mesh = object.data
    vertCnt = len(mesh.vertices)
    faceCnt = len(mesh.polygons)
    file.write(p('II', vertCnt, faceCnt))
    bBox = [object.bound_box[0][0],
            object.bound_box[0][2],
            object.bound_box[0][1],
            object.bound_box[6][0],
            object.bound_box[6][2],
            object.bound_box[6][1]]
    file.write(p('6f', bBox[0], bBox[1], bBox[2], bBox[3], bBox[4], bBox[5]))
    for v in mesh.vertices:
        file.write(p('3f', v.co.x, v.co.z, v.co.y))
    gameMtl = []
    for mat in mesh.materials:
        gameMtl.append(mat.stalkerMatID)
    for face in mesh.polygons:
        file.write(p('III', face.vertices[0],
                            face.vertices[2],
                            face.vertices[1]))
        vertID = face.vertices[0]
        vertex = mesh.vertices[vertID]
        if len(vertex.groups) == 1:
            groupID = vertex.groups[0].group
            vertexGroup = object.vertex_groups[groupID]
            vertexGroupName = vertexGroup.name
            sectorID = int(vertexGroupName)
        else:
            vertID = face.vertices[1]
            vertex = mesh.vertices[vertID]
            if len(vertex.groups) == 1:
                groupID = vertex.groups[0].group
                vertexGroup = object.vertex_groups[groupID]
                vertexGroupName = vertexGroup.name
                sectorID = int(vertexGroupName)
            else:
                vertID = face.vertices[2]
                vertex = mesh.vertices[vertID]
                if len(vertex.groups) == 1:
                    groupID = vertex.groups[0].group
                    vertexGroup = object.vertex_groups[groupID]
                    vertexGroupName = vertexGroup.name
                    sectorID = int(vertexGroupName)
        file.write(p('HH', gameMtl[face.material_index] | 0xc000, sectorID))

