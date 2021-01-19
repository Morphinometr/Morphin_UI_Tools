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

# <pep8 compliant>

bl_info = {
    "name": "Pie_Workspaces",
    "description": "Workspace Pie Menu",
    "author": "Morphin",
    "version": (0, 0, 1),
    "blender": (2, 90, 0),
    "location": "",
    "warning": "",
    "doc_url": "",
    "category": "Interface"
    }

import bpy
from bpy.types import Menu


# Pie Workspaces - W
class PIE_MT_Workspaces(Menu):
    bl_idname = "PIE_MT_workspaces"
    bl_label = "Pie Workspaces"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("class.layout", text="Layout", icon='SCENE_DATA')
        # 6 - RIGHT
        pie.operator("class.uvediting", text="UV Editing", icon='UV')
        # 2 - BOTTOM
        pie.operator("class.sculpting", text="Sculpting", icon='SCULPTMODE_HLT')
        # 8 - TOP
        pie.operator("class.shading", text="Shading", icon='NODE_MATERIAL')
        # 7 - TOP - LEFT
        pie.operator("class.animation", text="Animation", icon='NODE_MATERIAL')
        # 9 - TOP - RIGHT
        # 1 - BOTTOM - LEFT
        # 3 - BOTTOM - RIGHT
        
        
        #box = pie.split().column()
        #box.operator("mesh.remove_doubles", text="Merge By Distance", icon='NONE')
        #box.operator("mesh.delete", text="Only Edge & Faces", icon='NONE').type = 'EDGE_FACE'
        #box.operator("mesh.delete", text="Only Faces", icon='UV_FACESEL').type = 'ONLY_FACE'
        
        
class layout(bpy.types.Operator):
    bl_idname = "class.layout"
    bl_label = "layout"
    
    def execute(self, context):
        
        layout = self.layout
        bpy.context.window.workspace = bpy.data.workspaces['Layout']
        return {'FINISHED'}
    
class sculpting(bpy.types.Operator):
    bl_idname = "class.sculpting"
    bl_label = "sculpting"
    
    def execute(self, context):
        
        layout = self.layout
        bpy.context.window.workspace = bpy.data.workspaces['Sculpting']
        return {'FINISHED'}

class uvediting(bpy.types.Operator):
    bl_idname = "class.uvediting"
    bl_label = "uvediting"
    
    def execute(self, context):
        
        layout = self.layout
        bpy.context.window.workspace = bpy.data.workspaces['UV Editing']
        return {'FINISHED'}

class shading(bpy.types.Operator):
    bl_idname = "class.shading"
    bl_label = "shading"
    
    def execute(self, context):
        
        layout = self.layout
        bpy.context.window.workspace = bpy.data.workspaces['Shading']
        return {'FINISHED'}
    
class animation(bpy.types.Operator):
    bl_idname = "class.animation"
    bl_label = "animation"
    
    def execute(self, context):
        
        layout = self.layout
        bpy.context.window.workspace = bpy.data.workspaces['Animation']
        return {'FINISHED'}
    
    


classes = (
    PIE_MT_Workspaces,
    layout,
    sculpting,
    uvediting,
    shading,
    animation,
    
    )


addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        # Delete
        km = wm.keyconfigs.addon.keymaps.new(name='Window')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'CLICK_DRAG')
        kmi.properties.name = "PIE_MT_workspaces"
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
