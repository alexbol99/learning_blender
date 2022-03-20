import bpy

for idx in range(600):
    x = idx % 25
    y = idx // 25
    bpy.ops.mesh.primitive_monkey_add(size=0.2, location=(x, y, 1))
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.ops.object.shade_smooth()
    
