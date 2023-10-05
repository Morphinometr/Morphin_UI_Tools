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
    "name": "Pie Manipulator",
    "description": "Transform Manipulator Menu",
    "author": "pitiwazou, meta-androcto, Morphin",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "loacation": "PIE_MT_texture_paint_brushes",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
    }

import typing
import bpy
from bpy.types import Context, Menu, Operator
from bpy.props import EnumProperty, BoolProperty


class PIE_OT_Morph_Manupulators(Operator):
    bl_idname = "morph.manipulator"
    bl_label = "Pie Transform Manipulator"

    extend: BoolProperty(
        default=False,
    )
    type: EnumProperty(
        items=(
            ('TRANSLATE', "Move", ""),
            ('ROTATE', "Rotate", ""),
            ('SCALE', "Scale", ""),
            ('EXTEND_TRANSLATE', "Extend Translate", "" ),
            ('EXTEND_ROTATE', "Extend Rotate", ""),
            ('EXTEND_SCALE', "Extend Scale", ""),
        )
    )

    def execute(self, context):
        space_data = context.space_data
        space_data.show_gizmo_context = True

        attrs = (
            "show_gizmo_object_translate",
            "show_gizmo_object_rotate",
            "show_gizmo_object_scale",
        )
        attr_t, attr_r, attr_s = attrs
        attr_index = ('TRANSLATE', 'ROTATE', 'SCALE', 'EXTEND_TRANSLATE', 'EXTEND_ROTATE', 'EXTEND_SCALE').index(self.type)
        if attr_index > 2:
            attr_index -= 3
            self.extend = True
        else:
            self.extend = False
        
        attr_active = attrs[attr_index]

        if self.extend:
            print('extend')
            setattr(space_data, attr_active, not getattr(space_data, attr_active))
        else:
            for attr in attrs:
                setattr(space_data, attr, attr == attr_active)
        return {'FINISHED'}


class PIE_OT_Morph_Manupulators_default(Operator):
    bl_idname = "morph.manipulator_default"
    bl_label = "Pie Transform Manipulator"
    
    def execute(self, context):
        context.scene.transform_orientation_slots[1].type = 'DEFAULT'
        return {'FINISHED'}


class PIE_MT_morph_manipulator_orientation(Menu):
    bl_idname = "PIE_MT_morph_manipulator_orientation"
    bl_label = "Pie Manipulator Orientation"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        pie.operator("morph.manipulator_default", text="Default", icon='OBJECT_ORIGIN')
        pie.prop(context.scene.transform_orientation_slots[1], "type", expand=True)


# Pie Manipulators
class PIE_MT_Manipulator(Menu):
    bl_idname = "PIE_MT_morph_manipulator"
    bl_label = "Pie Manipulator"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        orientation_icons = {
            'DEFAULT': 'OBJECT_ORIGIN',
            'GLOBAL': 'ORIENTATION_GLOBAL',
            'LOCAL': 'ORIENTATION_LOCAL',
            'NORMAL': 'ORIENTATION_NORMAL',
            'GIMBAL': 'ORIENTATION_GIMBAL',
            'VIEW': 'ORIENTATION_VIEW',
            'CURSOR': 'ORIENTATION_CURSOR',
            'PARENT': 'ORIENTATION_PARENT'
        }
        current_orientation = context.scene.transform_orientation_slots[1].type
        orientation_icon = orientation_icons[current_orientation]
        orientation_text = "Orientation " + current_orientation.capitalize()
        
        # 4 - LEFT
        pie.operator("morph.manipulator", text="Rotate", icon='ORIENTATION_GIMBAL').type = 'ROTATE'
        # 6 - RIGHT
        pie.operator("morph.manipulator", text="Scale", icon='CON_CHILDOF').type = 'SCALE'
        # 2 - BOTTOM
        pie.operator("wm.context_toggle", text="Show/Hide Toggle", icon='NONE').data_path = "space_data.show_gizmo_context"
        # 8 - TOP
        pie.operator("morph.manipulator", text="Translate", icon='EMPTY_ARROWS').type = 'TRANSLATE'
        # 7 - TOP - LEFT
        pie.operator("morph.manipulator", text="Extend Translate", icon='ORIENTATION_GLOBAL').type = 'EXTEND_TRANSLATE'
        # 9 - TOP - RIGHT
        pie.operator("morph.manipulator", text="Extend Scale", icon='MOD_PARTICLE_INSTANCE').type = 'EXTEND_SCALE'
        # 1 - BOTTOM - LEFT
        pie.operator("morph.manipulator", text="Extend Rotate", icon='GIZMO').type = 'EXTEND_ROTATE'
        # 3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text=orientation_text, icon=orientation_icon).name = "PIE_MT_morph_manipulator_orientation"

classes = (
    PIE_OT_Morph_Manupulators,
    PIE_OT_Morph_Manupulators_default,
    PIE_MT_morph_manipulator_orientation,
    PIE_MT_Manipulator,
    
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()