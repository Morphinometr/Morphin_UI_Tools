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
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "loacation": "PIE_MT_texture_paint_brushes",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
    }

import bpy
from bpy.types import Menu, Operator
from bpy.props import EnumProperty


class PIE_OT_Morph_Manupulators(Operator):
    bl_idname = "morph.manipulator"
    bl_label = "Pie Transform Manipulator"

    type: EnumProperty(
        items=(
            ('TRANSLATE', "Move", ""),
            ('ROTATE', "Rotate", ""),
            ('SCALE', "Scale", ""),
            ('TRANSLATE_ROTATE', "Translate/Rotate", "" ),
        )
    )

    extend = False

    def invoke(self, context, event):
        self.extend = event.shift
        return self.execute(context)

    def execute(self, context):
        space_data = context.space_data
        space_data.show_gizmo_context = True

        attrs = (
            "show_gizmo_object_translate",
            "show_gizmo_object_rotate",
            "show_gizmo_object_scale",
        )
        
        attr_index = ('TRANSLATE', 'ROTATE', 'SCALE', 'TRANSLATE_ROTATE').index(self.type)

        if self.extend and attr_index < 3:
            attr_active = attrs[attr_index]
            setattr(space_data, attr_active, not getattr(space_data, attr_active))
            return {'FINISHED'}
        
        attrs_active = [False, False, False]
        
        if attr_index < 3:
            attrs_active[attr_index] = True
        else:
            attrs_active = [True, True, False]

        for attr, state in zip(attrs, attrs_active):
            setattr(space_data, attr, state)
        
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
        
        pie.prop(context.scene.transform_orientation_slots[1], "type", expand=True)
        pie.operator("morph.manipulator_default", text="Default", icon='OBJECT_ORIGIN')


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
        transform_pivots = {
            'BOUNDING_BOX_CENTER': 'PIVOT_BOUNDBOX',
            'CURSOR': 'PIVOT_CURSOR',
            'INDIVIDUAL_ORIGINS': 'PIVOT_INDIVIDUAL',
            'MEDIAN_POINT': 'PIVOT_MEDIAN',
            'ACTIVE_ELEMENT': 'PIVOT_ACTIVE'
        }

        gizmo_current_orientation = context.scene.transform_orientation_slots[1].type
        gizmo_orientation_icon = orientation_icons[gizmo_current_orientation]
        gizmo_orientation_text = "Gizmo Orientation: " + gizmo_current_orientation.capitalize()
        
        transform_orientation = context.scene.transform_orientation_slots[0].type
        transform_orientation_icon = orientation_icons[transform_orientation]
        transform_orientation_text = "Transform Orientation: " + transform_orientation.capitalize()

        transform_pivot = context.scene.tool_settings.transform_pivot_point
        transform_pivot_icon = transform_pivots[transform_pivot]
        transform_pivot_text = "Transform Pivot: " + transform_pivot.replace('_', ' ').title()

        # 4 - LEFT
        pie.operator("morph.manipulator", text="Rotate", icon='ORIENTATION_GIMBAL').type = 'ROTATE'
        # 6 - RIGHT
        pie.operator("morph.manipulator", text="Scale", icon='CON_CHILDOF').type = 'SCALE'
        # 2 - BOTTOM
        pie.operator("wm.context_toggle", text="Show/Hide Toggle", icon='NONE').data_path = "space_data.show_gizmo_context"
        # 8 - TOP
        pie.operator("morph.manipulator", text="Translate", icon='EMPTY_ARROWS').type = 'TRANSLATE'
        # 7 - TOP - LEFT
        pie.operator("wm.call_menu_pie", text=transform_pivot_text, icon=transform_pivot_icon).name = "VIEW3D_MT_pivot_pie"
        # 9 - TOP - RIGHT
        pie.operator("wm.call_menu_pie", text=transform_orientation_text, icon=transform_orientation_icon).name = "VIEW3D_MT_orientations_pie"
        # 1 - BOTTOM - LEFT
        pie.operator("morph.manipulator", text="Translate/Rotate", icon='GIZMO').type = 'TRANSLATE_ROTATE'
        # 3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text=gizmo_orientation_text, icon=gizmo_orientation_icon).name = "PIE_MT_morph_manipulator_orientation"

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