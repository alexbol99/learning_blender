from bpy import data as D, context as C
from mathutils import Matrix, Vector
from math import pi
import bmesh

# Create separate matrix for each transformation.
translate = Matrix.Translation(Vector((0.5, -0.25, 0.25)))

# Rotate 45 degrees around the z axis, (0.0, 0.0, 1.0).
rotate = Matrix.Rotation(pi / 4.0, 4, Vector((0.0, 0.0, 1.0)))

# Use a 4D vector to create a 4 x 4 nonuniform scale.
scale = Matrix.Diagonal(Vector((1.0, 0.5, 0.75, 1.0)))

# Composite affine transform from three separate matrices
# with the matmul operator (the at symbol, '@').
transform = translate @ rotate @ scale

bm = bmesh.new()
bmesh.ops.create_cube(bm, size=0.5, matrix=transform, calc_uvs=True)
mesh_data = D.meshes.new("Cube")
bm.to_mesh(mesh_data)
bm.free()
mesh_obj = D.objects.new(mesh_data.name, mesh_data)
C.collection.objects.link(mesh_obj)
