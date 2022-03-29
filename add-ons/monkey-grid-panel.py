import bpy


bl_info = {
    "name": "Monkey Grid",
    "author": "Alex Bol",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Object",
    "location": "Operator Search",
    "description": "More monkeys!",
    "warning": "",
    "doc_url": "",
    "tracker_url": ""
}


class MESH_OT_add_many_monkeys(bpy.types.Operator):
    """Let's spread some joy"""
    bl_idname = "mesh.add_many_monkeys"
    bl_label = "Monkey Default Grid"
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
        name="Size",
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
            y = idx // self.count_x
            bpy.ops.mesh.primitive_monkey_add(size=self.size, location=(x, y, 1))
            # bpy.ops.object.modifier_add(type='SUBSURF')
            # bpy.ops.object.shade_smooth()

        return {'FINISHED'}


class VIEW3D_PT_monkey_grid(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Monkeys Tool'
    bl_label = 'Add monkeys'

    def draw(self, context):
        col = self.layout.column(align=True)
        col.operator("mesh.add_many_monkeys",
                             text="Default grid",
                             icon="BLENDER")
        props = col.operator("mesh.add_many_monkeys",
                             text="Big grid with parameters",
                             icon="BLENDER")
        props.count_x = 10
        props.count_y = 10
        props.size = 0.9

        col = self.layout.column(align=True)
        col.prop(context.scene.cycles, 'preview_samples')
        if context.active_object is None:
            col.label(text='-no-active-object-')
        else:
            col.prop(context.active_object, 'hide_viewport')


def register():
    bpy.utils.register_class(MESH_OT_add_many_monkeys)
    bpy.utils.register_class(VIEW3D_PT_monkey_grid)


def unregister():
    bpy.utils.unregister_class(MESH_OT_add_many_monkeys)
    bpy.utils.unregister_class(VIEW3D_PT_monkey_grid)