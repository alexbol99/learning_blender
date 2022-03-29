import bpy


class MESH_OT_monkey_grid(bpy.types.Operator):
    """Let's spread some joy"""
    bl_idname = "mesh.monkey_grid"
    bl_label = "Monkey Grid"
    bl_options = {'REGISTER', 'UNDO'}

    count_x: bpy.props.IntProperty(
        name="X",
        description="Number of Monkeys in the X-direction",
        default=3,
        min=1,
        max=10
    )
    count_y: bpy.props.IntProperty(
        name="Y",
        description="Number of Monkeys in the Y-direction",
        default=2,
        min=1,
        max=10
    )
    
    size: bpy.props.FloatProperty(
        name="MonkeySize",
        description="Monkey size",
        default=0.2,
        min=0.01,
        max=1
    )
    

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D'
    
    
    def execute(self, context):
        for idx in range(self.count_x * self.count_y):
            x = idx % self.count_x
            y = idx // self.count_y
            bpy.ops.mesh.primitive_monkey_add(size=self.size,location=(x, y, 1))
            # bpy.ops.object.modifier_add(type='SUBSURF')
            # bpy.ops.object.shade_smooth()
            
        return {'FINISHED'}
    
    
def register():
    bpy.utils.register_class(MESH_OT_monkey_grid)
        
        
def unregister():
    bpy.utils.unregister_class(MESH_OT_monkey_grid)
    
    
if __name__ == "__main__":
    register()
    