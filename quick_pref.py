import bpy
bl_info = {"name": "QuickPref",
           "description": "Quick access to Preferences",
           "author": "Morphin",
           "version": (0, 0, 6),
           "blender": (2, 80, 0),
           "location": "View3d > View, Dopesheet > Action, Graph > View",
           "warning": "",
           "wiki_url": "",
           "tracker_url": "",
           "category": "3D View", }

    
class VIEW3D_OT_LocalViewCustom(bpy.types.Operator):
    """Toggles Local View without changing perspective"""
    bl_idname = "view3d.localview_custom"
    bl_label = "Local View without frame selected"

    
    @classmethod
    def poll(cls, context):
        if context.space_data.local_view:
            return True
        elif len(context.selected_objects) > 0 and context.active_object is not None:
            return True
        else:
            cls.poll_message_set("Expect selected objects")
        
    def execute(self, context):
        bpy.ops.view3d.localview(frame_selected=False)
        
        return {'FINISHED'}


class VIEW3D_PT_PanelQuickPref(bpy.types.Panel):
    """Creates a Panel in the scene context of the 3D view N panel"""
    
    bl_label = "QuickPref"
    bl_idname = "QUICK_PT_PREF"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    
    
    def draw(self, context):
        layout = self.layout
        column = layout.column(align=True)
        
        row = column.row(align=True)
        row.prop(context.preferences.inputs, "view_rotate_method", expand = True)
        
        column.operator("view3d.localview_custom", icon = 'OBJECT_HIDDEN', text = 'Local view')
        
        column.prop(context.preferences.inputs, "use_rotate_around_active")
        
        column.prop(context.preferences.edit, "use_mouse_depth_cursor")
        
        column.prop(context.preferences.inputs, "use_mouse_emulate_3_button")


class VIEW3D_PT_PanelAnimPref(bpy.types.Panel):
    """Creates a Panel in the scene context of the 3D view N panel"""
    
    bl_label = "QuickPref"
    bl_idname = "QUICK_PT_ANIM_PREF"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Action"
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column(align=True, heading="Insert Only")
        
        col.prop(context.preferences.edit, "use_keyframe_insert_available", text="Available")
        col.prop(context.preferences.edit, "use_keyframe_insert_needed", text="Needed")
        col = layout.column(align=True, heading="Show")
        col.prop(context.preferences.edit, "use_anim_channel_group_colors", text="Group")
        
        col = layout.column(align=True)
        col.label(text="New Curve:")
        col.prop(context.preferences.edit, "keyframe_new_interpolation_type", text="Interpolation")
        col.prop(context.preferences.edit, "keyframe_new_handle_type", text="Handles")


class VIEW3D_PT_PanelCurvePref(bpy.types.Panel):
    """Creates a Panel in the scene context of the 3D view N panel"""
    
    bl_label = "QuickPref"
    bl_idname = "QUICK_PT_CURVE_PREF"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_category = "View"
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        col = layout.column(align=True, heading="Insert Only")
        
        col.prop(context.preferences.edit, "use_keyframe_insert_needed", text="Available")
        col.prop(context.preferences.edit, "use_keyframe_insert_available", text="Needed")
        col = layout.column(align=True, heading="Show")
        col.prop(context.preferences.edit, "use_anim_channel_group_colors", text="Group")
        col.prop(context.preferences.edit, "show_only_selected_curve_keyframes", text="Selected")
        col.prop(context.preferences.edit, "fcurve_unselected_alpha", text="Unselected")


def morphin_view3d_header(self, context):
    mode_string = context.mode
    tool_settings = context.tool_settings
    if mode_string == 'OBJECT':
    

        row = self.layout.row(align=True)
        row.prop(tool_settings, "use_transform_data_origin", text="", icon="OBJECT_ORIGIN")


classes = (
    VIEW3D_OT_LocalViewCustom,
    VIEW3D_PT_PanelQuickPref,
    VIEW3D_PT_PanelAnimPref,
    VIEW3D_PT_PanelCurvePref,
    
    )
                    
                
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_HT_tool_header.append(morphin_view3d_header)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_HT_tool_header.remove(morphin_view3d_header)
        
if __name__ == "__main__":
    register()

