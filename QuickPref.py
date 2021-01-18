import bpy
bl_info = {"name": "QuickPref",
           "description": "Quick access to Preferences",
           "author": "Morphin",
           "version": (0, 0, 6),
           "blender": (2, 80, 0),
           "location": "View3d > Properties > QuickPref",
           "warning": "",
           "wiki_url": "",
           "tracker_url": "",
           "category": "3D View", }

    
    
class VIEW3D_OT_local_view_custom(bpy.types.Operator):
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




class VIEW3D_PT_panel_quickpref(bpy.types.Panel):
    """Creates a Panel in the scene context of the 3D view N panel"""
    
    bl_label = "QuickPref"
    bl_idname = "QUICK_PREF"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "View"
    
    
    def draw(self, context):
        layout = self.layout
      
              
        #row = layout.grid_flow(row_major = True, columns = 2, align = True, even_rows = True)
        column = layout.column(align=True)
        row = column.row(align=True)
        
        row.prop(context.preferences.inputs, "view_rotate_method", expand = True)
        #row = layout.row(align=True)
        column.operator("view3d.localview_custom", icon = 'OBJECT_HIDDEN', text = 'Local view')
                
        
        column.prop(context.preferences.inputs, "use_rotate_around_active")
        
        column.prop(context.preferences.edit, "use_mouse_depth_cursor")
        
        column.prop(context.preferences.inputs, "use_mouse_emulate_3_button")
        
        
                    
                
def register():
    bpy.utils.register_class(VIEW3D_PT_panel_quickpref)
    bpy.utils.register_class(VIEW3D_OT_local_view_custom)


def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_panel_quickpref)
    bpy.utils.unregister_class(VIEW3D_OT_local_view_custom)


