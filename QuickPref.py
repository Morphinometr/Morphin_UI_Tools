import bpy
bl_info = {"name": "QuickPref",
           "description": "Quick access to Preferences",
           "author": "Morphin",
           "version": (0, 0, 6),
           "blender": (2, 80, 0),
           "location": "View3d > Properties > View > QuickPref",
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
        else:
            return len(context.selected_objects) > 0 and context.active_object is not None
        #return context.active_object is not None
        
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
        
classes = (
    VIEW3D_OT_LocalViewCustom,
    VIEW3D_PT_PanelQuickPref,
    
    )
                    
                
def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

