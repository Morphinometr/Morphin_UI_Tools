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
    "name": "Pie_Brushes",
    "description": "Brushes Menu",
    "author": "Morphin",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "'B' click-drag",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
    }

import bpy
from bpy.types import Menu, Operator


# Pie Brush 'Texture Paint' Mode
class PIE_MT_texture_paint_brushes(Menu):
    bl_idname = "PIE_MT_texture_paint_brushes"
    bl_label = "Pie Texture Paint Brushes"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # display only avatlable brushes in current mode and current tool
        brushes = [brush for brush in bpy.data.brushes if brush.use_paint_image and 
                   brush.image_tool == context.workspace.tools.from_space_view3d_mode('PAINT_TEXTURE').idname[14:].upper()]
        brushes_additional = None
        
        # only 8 options available in pie menu
        if len(brushes) > 8:
            brushes_additional = brushes[8:]
            brushes = brushes[0:7]
        
        for i, brush in enumerate(brushes):
            # bottom option
            if i == 2:
                if brushes_additional:
                    box = pie.column()

                    for brush in brushes_additional:
                        box.context_pointer_set(name="brush", data=brush)
                        box.operator("paint.brush", text=brush.name)
                
            pie.context_pointer_set(name="brush", data=brush)
            pie.operator("paint.brush", text=brush.name)


class set_paint_brush(Operator):
    bl_idname = "paint.brush"
    bl_label = "layout"
    
    def execute(self, context):
        bpy.context.tool_settings.image_paint.brush = context.brush
        return {'FINISHED'}


classes = (
    PIE_MT_texture_paint_brushes,
    set_paint_brush
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()