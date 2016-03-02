# Copyright Les Fees Speciales 2015
# 
# voeu@les-fees-speciales.coop
# 
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
# 
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
# 
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
# 
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

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

