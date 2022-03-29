import bpy

name = "New Object"
mesh = bpy.data.meshes.new(name)
obj = bpy.data.objects.new(name, mesh)
col = bpy.data.collections.get("Collection")
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj

vertices = []
vertices.append([0.0, 1.0, 0.0])   # 0
vertices.append([-1.0, 0.0, 0.0])  # 1
vertices.append([0.0, -1.0, 0.0])  # 2
vertices.append([1.0, 0.0, 0.0])   # 3
vertices.append([0.0, 0.0, 1.0])   # 4

edges = []
edges.append([0,1])
edges.append([1,2])
edges.append([2,3])
edges.append([3,0])

edges.append([0,4])
edges.append([1,4])
edges.append([2,4])
edges.append([3,4])


faces = [
[0,1,2,3],
[0,1,4],
[1,2,4],
[2,3,4],
[3,0,4]
]


mesh.from_pydata(vertices, edges, faces)

# mod_skin = obj.modifiers.new('Skin','SKIN')

