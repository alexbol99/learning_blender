from bpy import data as D, context as C
from mathutils import Matrix
import bmesh

# Create a new BMesh instance.
bm = bmesh.new()

# Arguments for icosphere primitive.
subdivisions = 2
radius = 0.5
calc_uvs = True

# Create an identity 4 x 4 affine transform matrix:
# [(1.0, 0.0, 0.0, 0.0),
#  (0.0, 1.0, 0.0, 0.0),
#  (0.0, 0.0, 1.0, 0.0),
#  (0.0, 0.0, 0.0, 1.0)]
transform = Matrix.Identity(4)

# bmesh.ops contains primitive creation functions.
# The first argument, the BMesh is positional; the
# ensuing arguments are preceded by a keyword.
bmesh.ops.create_icosphere(
    bm,
    subdivisions=subdivisions,
    radius=radius,
    matrix=transform,
    calc_uvs=calc_uvs)

# Create new mesh data.
mesh_name = "Icosphere"
mesh_data = D.meshes.new(mesh_name)

# Convert BMesh to mesh data, then release BMesh.
bm.to_mesh(mesh_data)
bm.free()

# Create a new object which contains the mesh data.
mesh_obj = D.objects.new(mesh_data.name, mesh_data)

# Link the object to the scene collection.
C.collection.objects.link(mesh_obj)
