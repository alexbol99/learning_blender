
from bpy import data as D, context as C
from mathutils import noise, Vector
import math
import bmesh

bm = bmesh.new()

count = 96
phase = 3
min_rad = 0.0125
max_rad = 0.5

# Create spiral vertices.
i_range = range(0, count)
to_theta = phase * math.tau / count
to_fac = 1.0 / (count - 1.0)
spiral_verts = []
for i in i_range:
    fac = i * to_fac
    theta = i * to_theta
    rad = (1.0 - fac) * min_rad + fac * max_rad
    spiral_verts.append(bm.verts.new(
        (rad * math.cos(theta),
         rad * math.sin(theta), 0.0)))

# Connect vertices to previous to form edge.
spiral_edges = []
j_range = range(1, count)
for j in j_range:
    prev = spiral_verts[j - 1]
    curr = spiral_verts[j]
    spiral_edge = bm.edges.new([prev, curr])
    spiral_edges.append(spiral_edge)

# Create perpendiculars to original spiral.
ridge_verts = []
ridge_edges = []
interior_edges = []

# First ridge is a special case,
# as there is no previous point.
curr = spiral_verts[0]
curr_co = curr.co

# Find direction based on difference in points.
direc = spiral_verts[1].co - curr_co
perpendicular = Vector((direc.y, -direc.x, 0.0))
new_edge = curr_co + perpendicular

# Create ridge vertex.
ridge = bm.verts.new(new_edge)
ridge_verts.append(ridge)

# Create interior edges
interior_edge = bm.edges.new([curr, ridge])
interior_edges.append(interior_edge)

# Create edges perpendicular to each spiral vertex.
for j in j_range:
    prev = spiral_verts[j - 1]
    curr = spiral_verts[j]
    curr_co = curr.co

    # Find direction based on difference in points.
    direc = curr_co - prev.co
    perpendicular = Vector((direc.y, -direc.x, 0.0))
    new_edge = curr_co + perpendicular

    # Create ridge vertex.
    ridge = bm.verts.new(new_edge)
    ridge_verts.append(ridge)

    # Create interior edges.
    interior_edge = bm.edges.new([curr, ridge])
    interior_edges.append(interior_edge)

    # Connect ridge vertices to form ridge edges.
    prev = ridge_verts[j - 1]
    curr = ridge_verts[j]
    ridge_edge = bm.edges.new([prev, curr])
    ridge_edges.append(ridge_edge)

# Zip together spiral and ridge edges to form faces.
bottom_faces = []
for spiral, ridge in zip(spiral_edges, ridge_edges):
    sp_edge_vs = spiral.verts[:]
    rd_edge_vs = ridge.verts[:]

    # Reverse the edge direction for proper winding.
    rd_edge_vs.reverse()

    # Concatenate vertex lists.
    corners = sp_edge_vs + rd_edge_vs

    # Create 2D face.
    bottom_face = bm.faces.new(corners)
    bottom_faces.append(bottom_face)

# Create diamond pattern.
bmesh.ops.subdivide_edges(bm, edges=bm.edges, cuts=2, use_grid_fill=True)
bmesh.ops.unsubdivide(bm, verts=bm.verts, iterations=1)
bmesh.ops.split_edges(bm, edges=bm.edges)

# Scale down each face, then extrude.
min_height = 0.00125
max_height = 0.0125
min_scale = 0.75
max_scale = 0.9
noise_variety = 3.0
normal = Vector((0.0, 0.0, 1.0))

orig_faces = bm.faces[:]
for face in orig_faces:
    orig_verts = face.verts[:]

    # Find face center both for noise and for pivot.
    center = face.calc_center_median()

    # Introduce variety to pattern.
    fac = 0.5 + 0.5 * noise.noise(noise_variety * center)
    cmpl_fac = 1.0 - fac

    # Find amount to scale down face.
    u_scl = cmpl_fac * min_scale + fac * max_scale
    scale = Vector.Fill(3, u_scl)

    # Find amount to translate extruded face.
    extr_mag = cmpl_fac * min_height + fac * max_height
    extr = normal * extr_mag

    # Scale at "individual origins" pivot point.
    bmesh.ops.translate(bm, vec=-center, verts=orig_verts)
    bmesh.ops.scale(bm, vec=scale, verts=orig_verts)
    bmesh.ops.translate(bm, vec=center, verts=orig_verts)

    # Solidify then translate new face.
    new_geom = bmesh.ops.extrude_discrete_faces(bm, faces=[face])
    verts = new_geom["faces"][0].verts
    bmesh.ops.translate(bm, verts=verts, vec=extr)

    # Fill in bottom of extrusion.
    bm.faces.new(orig_verts)

# Ensure new bottom and sides of extrusion have proper normals.
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

# Method signature will change from Blender version 2.8x to 2.9 . Parameter
# vertex_only (bool) is replaced with affect, which accepts either 'EDGES' or
# 'VERTICES'.
geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
bmesh.ops.bevel(
    bm,
    geom=geom,
    affect='EDGES',
    offset_type='PERCENT',
    offset=5.0,
    segments=2,
    profile=0.5)

# Create object.
mesh_data = D.meshes.new("Spiral")
bm.to_mesh(mesh_data)
bm.free()
mesh_obj = D.objects.new(mesh_data.name, mesh_data)
C.collection.objects.link(mesh_obj)
