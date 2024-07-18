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
    "loacation": "PIE_MT_workspaces",
    "warning": "",
    "doc_url": "",
    "category": "Window"
    }

import bpy
from bpy.types import Menu, Operator, PropertyGroup
from bpy.props import StringProperty, EnumProperty

workspaces = [
    "Layout", "UV Editing"
]

class m_workspace():
    direction : EnumProperty
    workspace_name : StringProperty
    icon : StringProperty
    

class MT_Worspaces_prefs(PropertyGroup):
    workspaces : EnumProperty(
        items=(
            ("Left", "", "Layout"),
            ("Right", "", "Sculpting"),
            ("Bottom", "", "UV Editing"),
            ("Top", "", "UV Editing"),
        )
    )
    
    @property
    def filtered_icons(self):
        if self._filtered_icons is None:
            self._filtered_icons = []
            icon_filter = self._filter.upper()
            self.filtered_icons.clear()
            pr = prefs()

            icons = bpy.types.UILayout.bl_rna.functions[
                "prop"].parameters["icon"].enum_items.keys()
            for icon in icons:
                if icon == 'NONE' or \
                        icon_filter and icon_filter not in icon or \
                        not pr.show_brush_icons and "BRUSH_" in icon and \
                        icon != 'BRUSH_DATA' or \
                        not pr.show_matcap_icons and "MATCAP_" in icon or \
                        not pr.show_event_icons and (
                            "EVENT_" in icon or "MOUSE_" in icon
                        ) or \
                        not pr.show_colorset_icons and "COLORSET_" in icon:
                    continue
                self._filtered_icons.append(icon)

        return self._filtered_icons
    


# Pie Workspaces
class PIE_MT_Workspaces(Menu):
    bl_idname = "PIE_MT_workspaces"
    bl_label = "Workspaces"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("morph.workspace", text=workspaces[0], icon='SCENE_DATA').workspace = workspaces[0]
        # # 6 - RIGHT
        pie.operator("class.uvediting", text=workspaces[1], icon='UV_DATA')
        # # 2 - BOTTOM
        pie.operator("class.sculpting", text="Sculpting", icon='SCULPTMODE_HLT')
        # # 8 - TOP
        pie.operator("class.shading", text="Shading", icon='SHADING_RENDERED')
        # # 7 - TOP - LEFT
        pie.operator("class.animation", text="Animation", icon='ARMATURE_DATA')
        # # 9 - TOP - RIGHT
        pie.operator("class.txpaint", text="Texture Paint", icon='TPAINT_HLT')
        # # 1 - BOTTOM - LEFT
        pie.operator("screen.workspace_cycle", text="Prev", icon='TRIA_LEFT').direction = 'PREV'
        # # 3 - BOTTOM - RIGHT
        pie.operator("screen.workspace_cycle", text="Next", icon='TRIA_RIGHT').direction = 'NEXT'
        
        
class PIE_OT_workspace(Operator):
    bl_idname = "morph.workspace"
    bl_label = "workspace"
    
    workspace : StringProperty(name= "")
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces[self.workspace]
        return {'FINISHED'}
    
class PIE_OT_Sculpting(Operator):
    bl_idname = "class.sculpting"
    bl_label = "sculpting"
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces['Sculpting']
        return {'FINISHED'}

class PIE_OT_UVEditing(Operator):
    bl_idname = "class.uvediting"
    bl_label = "uvediting"
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces['UV Editing']
        return {'FINISHED'}

class PIE_OT_Shading(Operator):
    bl_idname = "class.shading"
    bl_label = "shading"
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces['Shading']
        return {'FINISHED'}
    
class PIE_OT_Animation(Operator):
    bl_idname = "class.animation"
    bl_label = "animation"
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces['Animation']
        return {'FINISHED'}
    
class PIE_OT_TxPaint(Operator):
    bl_idname = "class.txpaint"
    bl_label = "texture paint"
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces['Texture Paint']
        return {'FINISHED'}
    


classes = (
    MT_Worspaces_prefs,
    PIE_MT_Workspaces,
    PIE_OT_workspace,
    PIE_OT_Sculpting,
    PIE_OT_UVEditing,
    PIE_OT_Shading,
    PIE_OT_Animation,
    PIE_OT_TxPaint
    )


addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # wm = bpy.context.window_manager
    # if wm.keyconfigs.addon:
    #     km = wm.keyconfigs.addon.keymaps.new(name='Window')
    #     kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'CLICK_DRAG')
    #     kmi.properties.name = "PIE_MT_workspaces"
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
