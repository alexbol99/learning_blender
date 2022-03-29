from bpy import data as D, context as C
from mathutils import Vector
import math
import bmesh

bm = bmesh.new()
bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.25)

# The sequence bm.faces will increase in length
# per each iteration as new faces are added by
# the extrusion. It is important to _copy_
# the original faces of the mesh.
orig_faces = bm.faces[:]
extr_factor = 0.25
for face in orig_faces:

    # Ensure the normal has been updated.
    face.normal_update()
    face_nrm = face.normal.normalized()

    ext = bmesh.ops.extrude_discrete_faces(bm, faces=[face])
    new_faces = ext["faces"]
    for el in new_faces:
        el.normal_update()
        el_nrm = el.normal.normalized()

        # Find the dot product between two normals.
        dotp = el_nrm @ face_nrm

        # If they are approximately co-linear, translate.
        if abs(dotp) > 0.999999:
            extr = extr_factor * el_nrm
            bmesh.ops.translate(bm, vec=extr, verts=el.verts)

mesh_data = D.meshes.new("Extrusion")
bm.to_mesh(mesh_data)
bm.free()
mesh_obj = D.objects.new(mesh_data.name, mesh_data)
C.collection.objects.link(mesh_obj)
