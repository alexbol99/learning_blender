
from bpy import data as D, context as C
from mathutils import Matrix, Quaternion, Vector
import math
import bmesh


def create_torus(
        generate_uvs=True,
        location=Vector((0.0, 0.0, 0.0)),
        rotation=Quaternion((0.707107, -0.707107, 0.0, 0.0)),
        major_segments=32,
        minor_segments=16,
        major_radius=1.0,
        minor_radius=0.25,
        poly_type='QUAD',
        smooth_normals=True):

    # Validate inputs.
    sectors = max(3, major_segments)
    panels = max(3, minor_segments)
    rho0 = max(0.000001, major_radius)
    rho1 = max(0.000001, minor_radius)

    # Calculate theta from number of sectors in a ring.
    to_theta = math.tau / sectors
    j_range = range(0, sectors)
    sin_cos_theta = [(0.0, 0.0)] * sectors
    for j in j_range:
        theta = j * to_theta
        sin_cos_theta[j] = (math.sin(theta), math.cos(theta))

    # Calculate phi from number of panels in a sector.
    to_phi = math.tau / panels
    i_range = range(0, panels)
    sin_cos_phi = [(0.0, 0.0)] * panels
    for i in i_range:
        phi = i * to_phi
        sin_cos_phi[i] = (math.sin(phi), math.cos(phi))

    # Calculate Cartesian coordinates.
    len_vs = panels * sectors
    vs = [(0.0, 0.0, 0.0)] * len_vs
    k = 0
    for i in i_range:

        # The tuple at index i can be unpacked into
        # two named variables, separated by a comma.
        sin_phi, cos_phi = sin_cos_phi[i]

        # Major radius (rho0) determines donut hole size.
        # Minor radius (rho1) determines donut thickness.
        rho_cos_phi = rho0 + rho1 * cos_phi
        rho_sin_phi = rho1 * sin_phi

        for j in j_range:
            sin_theta, cos_theta = sin_cos_theta[j]

            # Donut hole opens onto the y axis.
            vs[k] = (rho_cos_phi * cos_theta,
                     -rho_sin_phi,
                     rho_cos_phi * sin_theta)
            k += 1

    # Generate vertex indices.
    # This list will be twice as long if triangles are used.
    len_fs = 0
    if poly_type is 'QUAD':
        len_fs = len_vs
    else:
        len_fs = len_vs * 2
    v_idcs = [(0, 0, 0)] * len_fs

    k = 0
    for i in i_range:
        i_v_next = (i + 1) % panels

        # Formula to convert 2D array indices to 1D index:
        # k = j + i * inner_arr_len
        v_off_curr = i * sectors
        v_off_next = i_v_next * sectors

        for j in j_range:
            j_v_next = (j + 1) % sectors

            # Indices for each corner of face.
            # v01 <-- v11
            #  |       ^
            #  v       |
            # v00 --> v10
            v00 = v_off_curr + j
            v10 = v_off_curr + j_v_next
            v11 = v_off_next + j_v_next
            v01 = v_off_next + j

            # Create quadrilaterals based on poly type.
            # Default to triangles.
            if poly_type is 'QUAD':
                v_idcs[k] = (v00, v10, v11, v01)
                k += 1
            else:
                v_idcs[k] = (v00, v10, v11)
                v_idcs[k + 1] = (v00, v11, v01)
                k += 2

    bm = bmesh.new()

    # Transfer vertex coordinates to Bmesh.
    bm_verts = []
    for v in vs:
        bm_vert = bm.verts.new(v)
        bm_verts.append(bm_vert)
    bm.verts.index_update()

    # Transfer face data to BMesh.
    bm_faces = []
    for idx_tuple in v_idcs:
        face_verts = []
        for idx in idx_tuple:
            vert = bm_verts[idx]
            face_verts.append(vert)
        bm_face = bm.faces.new(face_verts)
        bm_face.smooth = smooth_normals
        bm_faces.append(bm_face)
    bm.faces.index_update()

    # Optionally, add texture coordinates.
    if generate_uvs:

        # There is one more element per sector and per panel in texture
        # coordinates than above.
        sectors1 = sectors + 1
        panels1 = panels + 1
        len_vts = sectors1 * panels1
        vts = [(0.0, 0.0)] * len_vts

        # Calculate horizontal texture coordinate.
        tex_xs = [0.0] * sectors1
        to_s = 1.0 / sectors
        g_range = range(0, sectors1)
        for g in g_range:
            tex_xs[g] = g * to_s

        # Calculate vertical texture coordinate.
        tex_ys = [0.0] * panels1
        to_t = 1.0 / panels
        h_range = range(0, panels1)
        for h in h_range:
            tex_ys[h] = h * to_t

        # Combine horizontal and vertical.
        k = 0
        for h in h_range:
            t = tex_ys[h]
            for g in g_range:
                s = tex_xs[g]
                vts[k] = (s, t)
                k += 1

        # Unlike vertex indices above, there is no wraparound to index 0; mod
        # (%) is not used. This list matches the v_idcs list, despite the fact
        # that there are more vts than there are vs.
        vt_idcs = [(0, 0, 0)] * len_fs
        k = 0
        for i in i_range:
            vt_off_curr = i * sectors1
            vt_off_next = vt_off_curr + sectors1

            for j in j_range:
                j_vt_next = j + 1

                vt00 = vt_off_curr + j
                vt10 = vt_off_curr + j_vt_next
                vt11 = vt_off_next + j_vt_next
                vt01 = vt_off_next + j

                if poly_type is 'QUAD':
                    vt_idcs[k] = (vt00, vt10, vt11, vt01)
                    k += 1
                else:
                    vt_idcs[k] = (vt00, vt10, vt11)
                    vt_idcs[k + 1] = (vt00, vt11, vt01)
                    k += 2

        # Transfer UV coordinates to BMesh.
        bm_idx = 0
        uv_verify = bm.loops.layers.uv.verify()
        for bm_face in bm_faces:
            vt_idx_tup = vt_idcs[bm_idx]
            loop_idx = 0
            for bm_loop in bm_face.loops:
                loop_uv_layer = bm_loop[uv_verify]
                vt_idx = vt_idx_tup[loop_idx]
                loop_uv_layer.uv = vts[vt_idx]
                loop_idx += 1
            bm_idx += 1

    # Apply transformations.
    tr_mat = Matrix.Translation(location)
    rot_mat = rotation.to_matrix()
    rot_mat.resize_4x4()
    bmesh.ops.transform(bm,
                        matrix=tr_mat @ rot_mat,
                        space=Matrix.Identity(4),
                        verts=bm.verts)
    return bm


bm = create_torus()
mesh_data = D.meshes.new("Torus")
bm.to_mesh(mesh_data)
bm.free()
mesh_obj = D.objects.new(mesh_data.name, mesh_data)
C.collection.objects.link(mesh_obj)
