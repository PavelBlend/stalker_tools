

class ObjectFormat:
    class Version16:
        class Chunks:
            class Main:
                class Version:
                    id = 0x0900
                    version = 16
                class Flags:
                    id = 0x0903
                class Materials:
                    id = 0x0907
                class Meshes:
                    class Mesh:
                        class Version:
                            id = 0x1000
                            version = 17
                        class MeshName:
                            id = 0x1001
                        class Flags:
                            id = 0x1002
                        class BBox:
                            id = 0x1004
                        class Vertices:
                            id = 0x1005
                        class Faces:
                            id = 0x1006
                        class VMRefs:
                            id = 0x1008
                        class MaterialIndices:
                            id = 0x1009
                        class Options:
                            id = 0x1010
                        class UVs:
                            id = 0x1012
                        class SmoothGroups:
                            id = 0x1013
                    id = 0x0910
                class UserData:
                    id = 0x0912
                class Bones:
                    class Bone:
                        class Version:
                            id = 0x1
                            version = 2
                        class Def:
                            id = 0x2
                        class BindPose:
                            id = 0x3
                        class Material:
                            id = 0x4
                        class Shape:
                            id = 0x5
                        class IkJoint:
                            id = 0x6
                        class MassParams:
                            id = 0x7
                        class IkFlags:
                            id = 0x8
                        class BreakParams:
                            id = 0x9
                        class Friction:
                            id = 0x10
                    id = 0x0921
                class Revision:
                    id = 0x0922
                class LodReference:
                    id = 0x0925
                id = 0x7777

