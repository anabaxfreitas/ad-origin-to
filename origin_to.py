# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import bpy
from bpy.types import Operator, Panel
from mathutils import Vector

bl_info = {
    "name": "Set Origin to Bottom/Top",
    "blender": (2, 82, 0),
    "category": "Object",
    "description": "Set the origin of selected objects to their bottom or top based on their bounding box."
}

class SetOriginBase:
    bl_options = {'REGISTER', 'UNDO'}
    
    def calculate_origin_point(self, obj, use_bottom):
        print(f"Calculating origin point for object: {obj.name}, use_bottom: {use_bottom}")
        
        # Get evaluated mesh (with modifiers)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mesh = obj_eval.data
        print(f"Evaluated mesh obtained for object: {obj.name}")
        
        # Get world coordinates of all vertices
        world_verts = [obj.matrix_world @ v.co for v in mesh.vertices]
        print(f"Number of vertices found: {len(world_verts)}")
        if not world_verts:
            print("No vertices found, returning None")
            return None
            
        # Calculate bounding box dimensions
        min_x = min(v.x for v in world_verts)
        max_x = max(v.x for v in world_verts)
        min_y = min(v.y for v in world_verts)
        max_y = max(v.y for v in world_verts)
        min_z = min(v.z for v in world_verts)
        max_z = max(v.z for v in world_verts)
        print(f"Bounding box - min_x: {min_x}, max_x: {max_x}, min_y: {min_y}, max_y: {max_y}, min_z: {min_z}, max_z: {max_z}")
        
        # Calculate center point
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        target_z = min_z if use_bottom else max_z
        print(f"Calculated origin point: ({center_x}, {center_y}, {target_z})")
        
        return Vector((center_x, center_y, target_z))

class SetOriginBottomOperator(Operator, SetOriginBase):
    bl_idname = "object.origin_set_bottom"
    bl_label = "Set Origin to Bottom"
    
    def execute(self, context):
        print("Executing Set Origin to Bottom")
        original_cursor = context.scene.cursor.location.copy()
        original_active = context.active_object
        print(f"Original cursor location: {original_cursor}, Original active object: {original_active.name if original_active else 'None'}")
        
        for obj in context.selected_objects:
            print(f"Processing object: {obj.name}")
            if obj.type != 'MESH':
                print(f"Skipping object {obj.name}, not a mesh")
                continue
                
            origin_point = self.calculate_origin_point(obj, use_bottom=True)
            if not origin_point:
                print(f"Skipping object {obj.name}, no valid origin point")
                continue
                
            context.scene.cursor.location = origin_point
            print(f"Cursor moved to: {origin_point}")
            context.view_layer.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            print(f"Origin set for object: {obj.name}")
            
        context.scene.cursor.location = original_cursor
        context.view_layer.objects.active = original_active
        print("Restored original cursor location and active object")
        return {'FINISHED'}

class SetOriginTopOperator(Operator, SetOriginBase):
    bl_idname = "object.origin_set_top"
    bl_label = "Set Origin to Top"
    
    def execute(self, context):
        print("Executing Set Origin to Top")
        original_cursor = context.scene.cursor.location.copy()
        original_active = context.active_object
        print(f"Original cursor location: {original_cursor}, Original active object: {original_active.name if original_active else 'None'}")
        
        for obj in context.selected_objects:
            print(f"Processing object: {obj.name}")
            if obj.type != 'MESH':
                print(f"Skipping object {obj.name}, not a mesh")
                continue
                
            origin_point = self.calculate_origin_point(obj, use_bottom=False)
            if not origin_point:
                print(f"Skipping object {obj.name}, no valid origin point")
                continue
                
            context.scene.cursor.location = origin_point
            print(f"Cursor moved to: {origin_point}")
            context.view_layer.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            print(f"Origin set for object: {obj.name}")
            
        context.scene.cursor.location = original_cursor
        context.view_layer.objects.active = original_active
        print("Restored original cursor location and active object")
        return {'FINISHED'}

class OriginToolsPanel(Panel):
    bl_label = "Origin Tools"
    bl_idname = "VIEW3D_PT_origin_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.origin_set_bottom")
        layout.operator("object.origin_set_top")

def register():
    bpy.utils.register_class(SetOriginBottomOperator)
    bpy.utils.register_class(SetOriginTopOperator)
    bpy.utils.register_class(OriginToolsPanel)

def unregister():
    bpy.utils.unregister_class(SetOriginBottomOperator)
    bpy.utils.unregister_class(SetOriginTopOperator)
    bpy.utils.unregister_class(OriginToolsPanel)

if __name__ == "__main__":
    register()
