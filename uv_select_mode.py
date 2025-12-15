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
    "name": "UV Select Mode",
    "description": "Separete select island mode",
    "author": "Morphin",
    "version": (0, 0, 2),
    "blender": (5, 0, 0),
    "loacation": "morph.uv_select_mode",
    "warning": "",
    "doc_url": "",
    "category": "2D View"
    }

import bpy
from bpy.props import EnumProperty, BoolProperty


class VIEW2D_OT_uv_select_mode(bpy.types.Operator):
    """Separete select island mode"""
    bl_idname = "morph.uv_select_mode"
    bl_label = "UV Select Mode"
    
    extend : BoolProperty(
        name="Extend",
        default=False
    )

    expand : BoolProperty(
        name="Expand",
        default=False
    )

    type : EnumProperty(
        name="Type",
        description="UV Selection Mode",
        items=[
            ("VERT", "Vertex", "", "UV_VERTEXSEL", 0),
            ("EDGE", "Edge", "", "UV_EDGESEL", 1),
            ("FACE", "Face", "", "UV_FACESEL", 2),
        
        ],
        default="VERT",
    )

    @classmethod
    def poll(cls, context):
        return True
        
    def execute(self, context):
        if context.tool_settings.use_uv_select_sync:
            bpy.ops.mesh.select_mode(use_extend=self.extend, use_expand=self.expand, type=self.type, action='TOGGLE')
        
        if self.type == "VERT":
            bpy.ops.uv.select_mode(type="VERTEX")
        else:
            bpy.ops.uv.select_mode(type=self.type)

        context.tool_settings.use_uv_select_island = False

        return {'FINISHED'}


def register():
    bpy.utils.register_class(VIEW2D_OT_uv_select_mode)


def unregister():
    bpy.utils.unregister_class(VIEW2D_OT_uv_select_mode)

        
if __name__ == "__main__":
    register()
