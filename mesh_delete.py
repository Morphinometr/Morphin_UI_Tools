# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Mesh Delete",
    "description": "Shortcut for deleting mesh. It deletes the type that currently active",
    "author": "Morphin",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "loacation": "morph.delete_mesh",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
    }

import bpy


class VIEW3D_OT_delete_mesh(bpy.types.Operator):
    """Shortcut for deleting mesh. It deletes the type that currently active"""
    bl_idname = "morph.delete_mesh"
    bl_label = "Delete Mesh Shortcut"
    
    @classmethod
    def poll(cls, context):
        return context.object and context.object.mode == "EDIT"
        
    def execute(self, context):
        mode = bpy.context.tool_settings.mesh_select_mode
        if sum(tuple(mode)) > 1:
            bpy.ops.wm.call_menu(name="VIEW3D_MT_edit_mesh_delete")
        elif mode[0]:
            bpy.ops.mesh.delete(type='VERT')
        elif mode[1]:
            bpy.ops.mesh.delete(type='EDGE')
        elif mode[2]:
            bpy.ops.mesh.delete(type='FACE')
        
        
        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW3D_OT_delete_mesh)


def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_delete_mesh)

        
if __name__ == "__main__":
    register()
