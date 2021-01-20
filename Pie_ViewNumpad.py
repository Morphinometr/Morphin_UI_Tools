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
    "name": "Pie_Views",
    "description": "Viewport Numpad Menu",
    "author": "pitiwazou, meta-androcto, morphin, Martynas Žiemys",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "'C' click-drag",
    "warning": "",
    "doc_url": "",
    "category": "3D View"
    }

import bpy
from bpy.types import (
        Menu,
        Operator,
        )


# Pie views numpad
class PIE_MT_ViewNumpad(Menu):
    bl_idname = "PIE_MT_viewnumpad"
    bl_label = "Pie Views Menu"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()
        scene = context.scene
        rd = scene.render

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
        pie.operator("view3d.view_camera", text="View Cam", icon='VIEW_CAMERA')
        # 3 - BOTTOM - RIGHT
        pie.operator("view3d.view_persportho", text="Persp/Ortho", icon='VIEW_PERSPECTIVE')
        # LEFT EXTRA
        pie.separator()
        # RIGHT EXTRA
        pie.separator()
        # BOTTOM EXTRA
        other = pie.column()
        gap = other.column()
        gap.separator()
        gap.scale_y = 7
        #other_menu = other.box().column() #dark background
        other.scale_y=1.2
        other.scale_x=1.2
        
        box = other.grid_flow(columns=2, align=True, even_columns=True, even_rows=True, row_major=True)
                        
        #row
        box.operator("view3d.camera_to_view", text="Cam To View", icon='HIDE_OFF')
        box.operator("view3d.object_as_camera", text="Make Active", icon='VIEW_CAMERA')

        #row
        box.operator("view3d.view_all", text="View All", icon='SHADING_BBOX').center = True
        box.operator("view3d.view_selected", text="Selected", icon='VIS_SEL_11') 

        #row
        box.operator("view3d.localview", text="Local/Global", icon='RESTRICT_VIEW_ON')
        box.operator("screen.screen_full_area", text="Toggle Full", icon='IMAGE_BACKGROUND')
        
        #row
        box.prop(rd, "use_border", text="Border")
        if context.space_data.lock_camera is False:
            box.operator("wm.context_toggle", text="Lock Cam",
                         icon='LOCKED').data_path = "space_data.lock_camera"
        elif context.space_data.lock_camera is True:
            box.operator("wm.context_toggle", text="Unlock Cam",
                         icon='UNLOCKED').data_path = "space_data.lock_camera"

        icon_locked = 'LOCKED' if ob and ob.lock_rotation[0] is False else \
                      'UNLOCKED' if ob and ob.lock_rotation[0] is True else 'LOCKED'
        
        

classes = (
    PIE_MT_ViewNumpad,
    
    )

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Views numpad
        km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'C', 'CLICK_DRAG')
        kmi.properties.name = "PIE_MT_viewnumpad"
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
