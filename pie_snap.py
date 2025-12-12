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
    "name": "Pie Snap",
    "description": "Snap Pie Menu",
    "author": "Morphin",
    "blender": (2, 90, 0),
    "version": (0, 1, 0),
    "location": "PIE_MT_2DSnap, PIE_MT_3DSnap",
    "warning": "",
    "doc_url": "",
    "category": "3D View, UV Editor"
    }

import bpy
from bpy.types import Menu, Operator
from bpy.props import EnumProperty, BoolProperty
        

def get_pixel_snap_mode ():
    if bpy.app.version < (3, 4, 0):
        return bpy.context.space_data.uv_editor.pixel_snap_mode
    else:
        return bpy.context.space_data.uv_editor.pixel_round_mode


def set_pixel_snap_mode (mode:str):
    if bpy.app.version < (3, 4, 0):
        bpy.context.space_data.uv_editor.pixel_snap_mode = mode
    else:
        bpy.context.space_data.uv_editor.pixel_round_mode = mode


#Pie classes

class PIE_MT_3DSnap(Menu):
    bl_idname = "PIE_MT_3DSnap"
    bl_label = "Snap 3D"
       
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        settings = context.tool_settings

        types = [
            ("INCREMENT", "Increment", "SNAP_INCREMENT", settings.snap_elements_base),
            ("VERTEX", "Vertex", "SNAP_VERTEX", settings.snap_elements_base),
            ("FACE", "Face", "SNAP_FACE", settings.snap_elements_base),
            ("EDGE", "Edge", "SNAP_EDGE", settings.snap_elements_base),
            ("GRID", "Grid", "SNAP_GRID", settings.snap_elements_base),
            # ("VOLUME", "Volume", "SNAP_VOLUME", settings.snap_elements_base),
            ("FACE_PROJECT", "Face Project", "SNAP_FACE_CENTER", settings.snap_elements_individual),
            ("EDGE_MIDPOINT", "Midpoint", "SNAP_MIDPOINT", settings.snap_elements_base),
            # ("EDGE_PERPENDICULAR", "Perpendicular", "SNAP_PERPENDICULAR", settings.snap_elements_base),
        ]

        for type in types:
            on = type[0] in type[3]
            pie.operator("morph.snap3d", text=type[1], icon=type[2], depress=on).type = type[0]
        
        
        pie.operator("wm.call_panel", text= "Snap Options", icon="KEY_MENU").name = "VIEW3D_PT_snapping"
       
class PIE_MT_2DSnap(Menu):
    bl_idname = "PIE_MT_2DSnap"
    bl_label = "Snap UVs"
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        types = [
            ("INCREMENT", "Increment", "SNAP_INCREMENT"),
            ("VERTEX", "Vertex", "SNAP_VERTEX"),
            ("GRID", "Grid", "SNAP_GRID"),
        ]

        # 4 - LEFT
        on = "INCREMENT" in context.tool_settings.snap_uv_element
        pie.operator("morph.snap2d", text="Increment", icon="SNAP_INCREMENT", depress=on).type = "INCREMENT"
        # 6 - RIGHT
        on = "VERTEX" in context.tool_settings.snap_uv_element
        pie.operator("morph.snap2d", text="Vertex", icon="SNAP_VERTEX", depress=on).type = "VERTEX"
        # 2 - BOTTOM
        if get_pixel_snap_mode() == "CORNER":
            pie.operator("snap2d.corner", icon="CHECKBOX_HLT")
        else: 
            pie.operator("snap2d.corner",icon="CHECKBOX_DEHLT")
        # 8 - TOP
        pie.operator("snap2d.flip_y", icon="SORT_DESC")
        # 7 - TOP - LEFT
        on = "GRID" in context.tool_settings.snap_uv_element
        pie.operator("morph.snap2d", text="Grid", icon="SNAP_GRID", depress=on).type = "GRID"
        # 9 - TOP - RIGHT
        pie.operator("snap2d.flip_x", icon="FORWARD")
        # 1 - BOTTOM - LEFT
        if get_pixel_snap_mode() == "CENTER":
            pie.operator("snap2d.center", icon="CHECKBOX_HLT")
        else: 
            pie.operator("snap2d.center",icon="CHECKBOX_DEHLT")
        # 3 - BOTTOM - RIGHT
        if get_pixel_snap_mode() == "DISABLED":
            pie.operator("snap2d.disabled", icon="CHECKBOX_HLT")
        else: 
            pie.operator("snap2d.disabled",icon="CHECKBOX_DEHLT")


class PIE_OP_3DSnap(Operator):
    bl_idname = "morph.snap3d"
    bl_label = "Snap 3D"
    
    toggle : BoolProperty(
        name="Toggle",
        default=False
    )

    type : EnumProperty(
        name="Type",
        items=[
            ("INCREMENT", "Increment", ""),
            ("GRID", "Grid", ""),
            ("VERTEX", "Vertex", ""),
            ("EDGE", "Edge", ""),
            ("FACE", "Face", ""),
            ("VOLUME", "Volume", ""),
            ("EDGE_MIDPOINT", "Midpoint", ""),
            ("EDGE_PERPENDICULAR", "Perpendicular", ""),
            ("FACE_PROJECT", "Face Project", "")
        ]
    )

    def invoke(self, context, event):
        self.toggle = event.shift
        return self.execute(context)

    def execute(self, context):
        settings = context.tool_settings

        if self.type == "FACE_PROJECT":
            settings.snap_elements_individual = {self.type}
            return {"FINISHED"}

        if self.toggle:
            settings.snap_elements ^= {self.type}
        else:
            settings.snap_elements = {self.type}
        
        if self.type == "INCREMENT":
            settings.use_snap_grid_absolute = False
        return {"FINISHED"}

class PIE_OP_2DSnap(Operator):
    bl_idname = "morph.snap2d"
    bl_label = "Snap 2D"
    
    toggle : BoolProperty(
        name="Toggle",
        default=False
    )

    type : EnumProperty(
        name="Type",
        items=[
            ("INCREMENT", "Increment", ""),
            ("GRID", "Grid", ""),
            ("VERTEX", "Vertex", ""),
        ]
    )

    def invoke(self, context, event):
        self.toggle = event.shift
        return self.execute(context)

    def execute(self, context):
        settings = context.tool_settings
        if self.toggle:
            settings.snap_uv_element ^= {self.type}
        else:
            settings.snap_uv_element = {self.type}
        

        return {"FINISHED"}


class PIE_OT_2DCorner(bpy.types.Operator):
    bl_idname = "snap2d.corner"
    bl_label = "Corner"
    bl_description = "Snap UVs to pixel corners. Overrites other snap settings"
    
    def execute(self, context):
        set_pixel_snap_mode("CORNER")
        return {"FINISHED"}

class PIE_OT_2DCenter(bpy.types.Operator):
    bl_idname = "snap2d.center"
    bl_label = "Center"
    bl_description = "Snap UVs to pixel centers. Overrites other snap settings" 
    
    def execute(self, context):
        set_pixel_snap_mode("CENTER")
        return {"FINISHED"}

class PIE_OT_2DDisabled(bpy.types.Operator):
    bl_idname = "snap2d.disabled"
    bl_label = "Disabled"
    bl_description = "Disable snapping UVs to pixels"
    
    def execute(self, context):
        set_pixel_snap_mode("DISABLED")
        return {"FINISHED"}

class PIE_OT_2DFlipX(bpy.types.Operator):
    bl_idname = "snap2d.flip_x"
    bl_label = "Flip UVs X"
    bl_description = "Flip selected UVs in X axis"
    
    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))
        return {"FINISHED"}

class PIE_OT_2DFlipY(bpy.types.Operator):
    bl_idname = "snap2d.flip_y"
    bl_label = "Flip UVs Y"
    bl_description = "Flip selected UVs in Y axis"
    
    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))
        return {"FINISHED"}



classes = (
    PIE_MT_3DSnap,
    PIE_MT_2DSnap,
    PIE_OP_3DSnap,
    PIE_OP_2DSnap,
    PIE_OT_2DCorner,
    PIE_OT_2DCenter,
    PIE_OT_2DDisabled,
    PIE_OT_2DFlipX,
    PIE_OT_2DFlipY
    )

addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # wm = bpy.context.window_manager
    # if wm.keyconfigs.addon:
    #     km = wm.keyconfigs.addon.keymaps.new(name="3D View Generic", space_type="VIEW_3D")
    #     kmi = km.keymap_items.new("wm.call_menu_pie", "S", "CLICK_DRAG")
    #     kmi.properties.name = "PIE_MT_3DSnap"
    #     addon_keymaps.append((km, kmi))
        
    #     km = wm.keyconfigs.addon.keymaps.new(name="UV Editor")
    #     kmi = km.keymap_items.new("wm.call_menu_pie", "S", "CLICK_DRAG")
    #     kmi.properties.name = "PIE_MT_2DSnap"
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