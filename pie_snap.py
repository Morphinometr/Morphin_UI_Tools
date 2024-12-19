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
    "version": (0, 0, 2),
    "location": "PIE_MT_2DSnap, PIE_MT_3DSnap",
    "warning": "",
    "doc_url": "",
    "category": "3D View, UV Editor"
    }

import bpy
from bpy.types import Menu
        

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
        
        # 4 - LEFT
        pie.operator("snap3d.increment", icon='SNAP_INCREMENT')
        # 6 - RIGHT
        pie.operator("snap3d.vertex", icon='SNAP_VERTEX')
        # 2 - BOTTOM
        pie.operator("snap3d.face", icon='SNAP_FACE')
        # 8 - TOP
        pie.operator("snap3d.edge", icon='SNAP_EDGE')
        # 7 - TOP - LEFT
        pie.operator("snap3d.grid", icon='SNAP_GRID')
        # 9 - TOP - RIGHT
        pie.operator("snap3d.volume", icon='SNAP_VOLUME')
        # 1 - BOTTOM - LEFT
        pie.operator("snap3d.edge_center", icon='SNAP_MIDPOINT')
        # 3 - BOTTOM - RIGHT
        pie.operator("snap3d.edge_perpendicular", icon='SNAP_PERPENDICULAR')
       
class PIE_MT_2DSnap(Menu):
    bl_idname = "PIE_MT_2DSnap"
    bl_label = "Snap UVs"
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        # 4 - LEFT
        pie.operator("snap2d.increment", icon='SNAP_INCREMENT')
        # 6 - RIGHT
        pie.operator("snap2d.vertex", icon='SNAP_VERTEX')
        # 2 - BOTTOM
        if get_pixel_snap_mode() == "CORNER":
            pie.operator("snap2d.corner", icon='CHECKBOX_HLT')
        else: 
            pie.operator("snap2d.corner",icon='CHECKBOX_DEHLT')
        # 8 - TOP
        pie.operator("snap2d.flip_y", icon='SORT_DESC')
        # 7 - TOP - LEFT
        pie.operator("snap2d.grid", icon='SNAP_GRID')
        # 9 - TOP - RIGHT
        pie.operator("snap2d.flip_x", icon='FORWARD')
        # 1 - BOTTOM - LEFT
        if get_pixel_snap_mode() == "CENTER":
            pie.operator("snap2d.center", icon='CHECKBOX_HLT')
        else: 
            pie.operator("snap2d.center",icon='CHECKBOX_DEHLT')
        # 3 - BOTTOM - RIGHT
        if get_pixel_snap_mode() == "DISABLED":
            pie.operator("snap2d.disabled", icon='CHECKBOX_HLT')
        else: 
            pie.operator("snap2d.disabled",icon='CHECKBOX_DEHLT')

#3D View classes

class PIE_OT_3DIncrement(bpy.types.Operator):
    bl_idname = "snap3d.increment"
    bl_label = "Increment"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'INCREMENT'}
        bpy.context.tool_settings.use_snap_grid_absolute = False
        return {'FINISHED'}
    
class PIE_OT_3DGrid(bpy.types.Operator):
    bl_idname = "snap3d.grid"
    bl_label = "Grid"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'INCREMENT'}
        bpy.context.tool_settings.use_snap_grid_absolute = True
        return {'FINISHED'}

class PIE_OT_3DVertex(bpy.types.Operator):
    bl_idname = "snap3d.vertex"
    bl_label = "Vertex"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'VERTEX'}
        return {'FINISHED'}

class PIE_OT_3DFace(bpy.types.Operator):
    bl_idname = "snap3d.face"
    bl_label = "Face"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'FACE'}
        return {'FINISHED'}

class PIE_OT_3DEdge(bpy.types.Operator):
    bl_idname = "snap3d.edge"
    bl_label = "Edge"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'EDGE'}
        return {'FINISHED'}

class PIE_OT_3DEdgeCenter(bpy.types.Operator):
    bl_idname = "snap3d.edge_center"
    bl_label = "Edge center"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'EDGE_MIDPOINT'}
        return {'FINISHED'}
    
class PIE_OT_3DEdgePerpendicular(bpy.types.Operator):
    bl_idname = "snap3d.edge_perpendicular"
    bl_label = "Edge perpendicular"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'EDGE_PERPENDICULAR'}
        return {'FINISHED'}
    
class PIE_OT_3DVolume(bpy.types.Operator):
    bl_idname = "snap3d.volume"
    bl_label = "Volume"
    
    def execute(self, context):
        bpy.context.tool_settings.snap_elements = {'VOLUME'}
        return {'FINISHED'}

#2D View classes

class PIE_OT_2DIncrement(bpy.types.Operator):
    bl_idname = "snap2d.increment"
    bl_label = "Increment"
    bl_description = "Set snaping to grid increments. Custom grid can be set in overlays"
    
    def execute(self, context):
        if bpy.app.version < (4, 2, 0):
            bpy.context.tool_settings.snap_uv_element = 'INCREMENT'
            bpy.context.tool_settings.use_snap_uv_grid_absolute = False
        else:
            bpy.context.tool_settings.snap_uv_element = {'INCREMENT'}
        return {'FINISHED'}

class PIE_OT_2DGrid(bpy.types.Operator):
    bl_idname = "snap2d.grid"
    bl_label = "Grid"
    bl_description = "Set snaping to grid points. Custom grid can be set in overlays"
    
    def execute(self, context):
        if bpy.app.version < (4, 2, 0):
            bpy.context.tool_settings.snap_uv_element = 'INCREMENT'
            bpy.context.tool_settings.use_snap_uv_grid_absolute = True
        else:
            bpy.context.tool_settings.snap_uv_element = {'GRID'}
        return {'FINISHED'}
    
class PIE_OT_2DVertex(bpy.types.Operator):
    bl_idname = "snap2d.vertex"
    bl_label = "Vertex"
    bl_description = "Set snaping to UV vertices"
    
    def execute(self, context):
        if bpy.app.version < (4, 2, 0):
            bpy.context.tool_settings.snap_uv_element = 'VERTEX'
        else:
            bpy.context.tool_settings.snap_uv_element = {'VERTEX'}
        return {'FINISHED'}

class PIE_OT_2DCorner(bpy.types.Operator):
    bl_idname = "snap2d.corner"
    bl_label = "Corner"
    bl_description = "Snap UVs to pixel corners. Overrites other snap settings"
    
    def execute(self, context):
        set_pixel_snap_mode('CORNER')
        return {'FINISHED'}

class PIE_OT_2DCenter(bpy.types.Operator):
    bl_idname = "snap2d.center"
    bl_label = "Center"
    bl_description = "Snap UVs to pixel centers. Overrites other snap settings" 
    
    def execute(self, context):
        set_pixel_snap_mode('CENTER')
        return {'FINISHED'}

class PIE_OT_2DDisabled(bpy.types.Operator):
    bl_idname = "snap2d.disabled"
    bl_label = "Disabled"
    bl_description = "Disable snapping UVs to pixels"
    
    def execute(self, context):
        set_pixel_snap_mode('DISABLED')
        return {'FINISHED'}

class PIE_OT_2DFlipX(bpy.types.Operator):
    bl_idname = "snap2d.flip_x"
    bl_label = "Flip UVs X"
    bl_description = "Flip selected UVs in X axis"
    
    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(True, False, False))
        return {'FINISHED'}

class PIE_OT_2DFlipY(bpy.types.Operator):
    bl_idname = "snap2d.flip_y"
    bl_label = "Flip UVs Y"
    bl_description = "Flip selected UVs in Y axis"
    
    def execute(self, context):
        bpy.ops.transform.mirror(constraint_axis=(False, True, False))
        return {'FINISHED'}



classes = (
    PIE_MT_3DSnap,
    PIE_MT_2DSnap,
    PIE_OT_3DIncrement,
    PIE_OT_3DVertex,
    PIE_OT_3DFace,
    PIE_OT_3DGrid,
    PIE_OT_3DEdge,
    PIE_OT_3DEdgeCenter,
    PIE_OT_3DEdgePerpendicular,
    PIE_OT_3DVolume,
    PIE_OT_2DIncrement,
    PIE_OT_2DGrid,
    PIE_OT_2DVertex,
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
    #     km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D')
    #     kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'CLICK_DRAG')
    #     kmi.properties.name = "PIE_MT_3DSnap"
    #     addon_keymaps.append((km, kmi))
        
    #     km = wm.keyconfigs.addon.keymaps.new(name='UV Editor')
    #     kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'CLICK_DRAG')
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