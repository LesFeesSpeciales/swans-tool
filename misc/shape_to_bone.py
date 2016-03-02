import bpy


def main(context):
    selected = context.selected_objects[:]
    selected.remove(context.object)
    obj = selected[0]
    pbone = context.active_pose_bone

    mesh_copy = obj.to_mesh(context.scene, True, 'PREVIEW')
    mesh_copy.name = 'WGT_' + pbone.name
    obj_copy = bpy.data.objects.new('WGT_' + pbone.name, mesh_copy)
    context.scene.objects.link(obj_copy)

#    obj_copy.matrix_world.identity()
    obj_copy.layers = [False if i != 19 else True for i in range(20)]

    b_length = pbone.bone.length

    pbone.custom_shape = obj_copy
    pbone.bone.show_wire = True

    for v in obj_copy.data.vertices:
        v.co = (1 / b_length) * pbone.matrix.inverted() * obj.matrix_world * v.co


class ShapeToBone(bpy.types.Operator):
    """Reposition selected mesh so that the active bone takes the mesh as custom shape.
    You need to be in pose mode with a mesh object selected."""
    bl_idname = "pose.shape_to_bone"
    bl_label = "Shape To Bone"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 1 and context.active_pose_bone is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ShapeToBone)


def unregister():
    bpy.utils.unregister_class(ShapeToBone)


if __name__ == "__main__":
    register()

