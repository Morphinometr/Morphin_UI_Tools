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
    "version": (0, 0, 2),
    "blender": (2, 90, 0),
    "loacation": "PIE_MT_workspaces",
    "warning": "",
    "doc_url": "",
    "category": "Window"
    }

import bpy
from bpy.types import Menu, Operator, PropertyGroup
from bpy.props import StringProperty, EnumProperty

workspaces = {
    "Layout" : "SCENE_DATA",
    "UV Editing" : "UV_DATA",
    "Sculpting" : "SCULPTMODE_HLT",
    "Shading" : "SHADING_RENDERED",
    "Animation" : "ARMATURE_DATA",
    "Texture Paint" : "TPAINT_HLT",
    "Geometry Nodes" : "GEOMETRY_NODES",
    "Scripting" : "FILE_SCRIPT"
}

# class m_workspace():
#     direction : EnumProperty
#     workspace_name : StringProperty
#     icon : StringProperty
    

# class MT_Worspaces_prefs(PropertyGroup):
#     workspaces : EnumProperty(
#         items=(
#             ("Left", "", "Layout"),
#             ("Right", "", "Sculpting"),
#             ("Bottom", "", "UV Editing"),
#             ("Top", "", "UV Editing"),
#         )
#     )
    
#     @property
#     def filtered_icons(self):
#         if self._filtered_icons is None:
#             self._filtered_icons = []
#             icon_filter = self._filter.upper()
#             self.filtered_icons.clear()
#             pr = prefs()

#             icons = bpy.types.UILayout.bl_rna.functions[
#                 "prop"].parameters["icon"].enum_items.keys()
#             for icon in icons:
#                 if icon == "NONE" or \
#                         icon_filter and icon_filter not in icon or \
#                         not pr.show_brush_icons and "BRUSH_" in icon and \
#                         icon != "BRUSH_DATA" or \
#                         not pr.show_matcap_icons and "MATCAP_" in icon or \
#                         not pr.show_event_icons and (
#                             "EVENT_" in icon or "MOUSE_" in icon
#                         ) or \
#                         not pr.show_colorset_icons and "COLORSET_" in icon:
#                     continue
#                 self._filtered_icons.append(icon)

#         return self._filtered_icons
    


# Pie Workspaces
class PIE_MT_Workspaces(Menu):
    bl_idname = "PIE_MT_workspaces"
    bl_label = "Workspaces"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        for name, icon in workspaces.items():
            pie.operator("morph.workspace", text=name, icon=icon).workspace = name
        
        
class PIE_OT_workspace(Operator):
    bl_idname = "morph.workspace"
    bl_label = "workspace"
    
    workspace : StringProperty(name= "")
    
    def execute(self, context):
        bpy.context.window.workspace = bpy.data.workspaces[self.workspace]
        return {"FINISHED"}
    

classes = (
    # MT_Worspaces_prefs,
    PIE_MT_Workspaces,
    PIE_OT_workspace,
    )


addon_keymaps = []


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # wm = bpy.context.window_manager
    # if wm.keyconfigs.addon:
    #     km = wm.keyconfigs.addon.keymaps.new(name="Window")
    #     kmi = km.keymap_items.new("wm.call_menu_pie", "W", "CLICK_DRAG")
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