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
    "name": "Pie Views",
    "description": "Viewport Numpad Menu",
    "author": "Morphin",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "PIE_MT_viewnumpad",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
    }

import bpy
from bpy.types import Menu


class PIE_MT_morph_view_options(Menu):
    bl_idname = "PIE_MT_morph_view_options"
    bl_label = "View Options"
    
    def draw(self, context):
        pie = self.layout.menu_pie()

        # 4 - LEFT
        pie.operator("view3d.view_selected", text="Selected", icon='VIS_SEL_11')
        # 6 - RIGHT
        pie.operator("view3d.view_all", text="All", icon='STICKY_UVS_DISABLE')
        # 2 - BOTTOM
        pie.operator("view3d.view_camera", text="View Cam", icon='VIEW_CAMERA')
        # 8 - TOP
        pie.operator("view3d.camera_to_view", text="Cam To View", icon='HIDE_OFF')
        # 7 - TOP - LEFT
        pie.prop(context.scene.render, "use_border", text="Border", icon='SELECT_SET')
        # 9 - TOP - RIGHT
        pie.prop(context.space_data, "lock_camera", text="Lock Camera", icon='VIEW_LOCKED')
        # 1 - BOTTOM - LEFT
        pie.operator("view3d.object_as_camera", text="Make Active", icon='OUTLINER_DATA_CAMERA')
        # 3 - BOTTOM - RIGHT
        pie.operator("view3d.view_persportho", text="Persp/Ortho", icon='VIEW_PERSPECTIVE')
        

# Pie views numpad
class PIE_MT_ViewNumpad(Menu):
    bl_idname = "PIE_MT_viewnumpad"
    bl_label = "Pie Views Menu"

    def draw(self, context):
        pie = self.layout.menu_pie()

        # 4 - LEFT
        pie.operator("view3d.view_axis", text="Left", icon='TRIA_LEFT').type = 'LEFT'
        # 6 - RIGHT
        pie.operator("view3d.view_axis", text="Right", icon='TRIA_RIGHT').type = 'RIGHT'
        # 2 - BOTTOM
        pie.operator("view3d.view_axis", text="Bottom", icon='TRIA_DOWN').type = 'BOTTOM'
        # 8 - TOP
        pie.operator("view3d.view_axis", text="Top", icon='TRIA_UP').type = 'TOP'
        # 7 - TOP - LEFT
        pie.operator("view3d.view_axis", text="Front", icon='EVENT_F').type = 'FRONT'
        # 9 - TOP - RIGHT
        pie.operator("view3d.view_axis", text="Back", icon='EVENT_B').type = 'BACK'
        # 1 - BOTTOM - LEFT
        pie.operator("view3d.localview", text="Local/Global", icon='RESTRICT_VIEW_ON').frame_selected=False
        # 3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text= 'View Options', icon='RESTRICT_VIEW_OFF').name = "PIE_MT_morph_view_options"
        

classes = (
    PIE_MT_ViewNumpad,
    PIE_MT_morph_view_options,
    
    )

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # wm = bpy.context.window_manager
    # if wm.keyconfigs.addon:
    #     # Views numpad
    #     km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    #     kmi = km.keymap_items.new('wm.call_menu_pie', 'C', 'CLICK_DRAG')
    #     kmi.properties.name = "PIE_MT_viewnumpad"
    #     addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # wm = bpy.context.window_manager
    # kc = wm.keyconfigs.addon
    # if kc:
    #     for km, kmi in addon_keymaps:
    #         km.keymap_items.remove(kmi)
    # addon_keymaps.clear()


if __name__ == "__main__":
    register()
