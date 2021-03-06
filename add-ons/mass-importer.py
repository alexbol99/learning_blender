bl_info = {
    "name": "SfA: Mass Importer",
    "author": "Alex Bol",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Import",
    "location": "3D Viewport",
    "description": "Mass-import OBJ files and keep track of where they came from",
    "warning": "",
    "doc_url": "",
    "tracker_url": ""
}

import pathlib
import bpy


def mass_import_path(scene) -> pathlib.Path:
    abspath = bpy.path.abspath(scene.mass_import_path)
    return pathlib.Path(abspath)


# Custom operator to import many obj files
class IMPORT_SCENE_OT_obj_mass(bpy.types.Operator):
    bl_idname = 'import_scene.obj_mass'
    bl_label = "Mass-import OBJs"

    def execute(self, context):
        # bpy.ops.import_scene.obj(filepath='')
        # find the OBJ files
        import_path = mass_import_path(context.scene)
        for import_fpath in import_path.glob('*.obj'):
            bpy.ops.import_scene.obj(filepath=str(import_fpath))
            for imported_ob in context.selected_objects:
                imported_ob.mass_import_fname = import_fpath.name

        return {'FINISHED'}

#       self.report(
#            {'ERROR'},
#            f'No code to load from {abspath}'
#        )
#        return {'CANCELLED'}


class IMPORT_SCENE_OT_obj_reload(bpy.types.Operator):
    bl_idname = 'import_scene.obj_reload'
    bl_label = "Reload mass-imported object"


    def execute(selfself, context):
        ob = context.object
        # Store what we want to remember
        mass_import_fname = ob.mass_import_fname
        matrix_world = ob.matrix_world.copy()

        # Remove object from scene == unlink from collections
        # create a list as new copy of collections in order to
        # avoid changing users_collections inside a loop
        for collection in list(ob.users_collection):
            collection.objects.unlink(ob)

        # if object is not in use anywhere, remove it from Blender's memory
        if ob.users == 0:
            bpy.data.objects.remove(ob)
        del ob      # remove name from Python's memory

        # Load OBJ file
        import_path = mass_import_path(context.scene)
        import_fpath = import_path / mass_import_fname
        bpy.ops.import_scene.obj(filepath=str(import_fpath))

        # Restore what we remembered
        for imported_ob in context.selected_objects:
            imported_ob.mass_import_fname = import_fpath.name
            imported_ob.matrix_world = matrix_world

        return {'FINISHED'}


class VIEW3D_PT_mass_import(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Mass Importer'
    bl_label = 'Mass import'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.prop(context.scene, 'mass_import_path')
        col.operator('import_scene.obj_mass')

        col = layout.column(align=True)
        if context.object:
            col.prop(context.object, 'mass_import_fname')
            col.operator('import_scene.obj_reload')
        else:
            col.label(text='-no active object-')



blender_classes = [
    VIEW3D_PT_mass_import,
    IMPORT_SCENE_OT_obj_mass,
    IMPORT_SCENE_OT_obj_reload
]


def register():
    bpy.types.Scene.mass_import_path = bpy.props.StringProperty(
        name='OBJ Folder',
        subtype='DIR_PATH',
    )
    bpy.types.Object.mass_import_fname = bpy.props.StringProperty(
        name='OBJ File',
    )
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    del bpy.types.Scene.mass_import_path
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)


