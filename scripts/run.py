import pydevd
import sys
import bpy

# This is how you run the blender debug client
sys.path.append("/Applications/PyCharm.app/Contents/debug-eggs/pydevd-pycharm.egg")
pydevd.settrace("localhost", port=1090, stdoutToServer=True, stderrToServer=True, suspend=False)

# This is how you enable the blender command args
sys.argv = [__file__] + (sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])

print(f"all objects in the scene before {bpy.data.objects.values()}")

bpy.ops.mesh.primitive_cube_add()

print(f"all objects in the scene after{bpy.data.objects.values()}")

bpy.ops.wm.save_as_mainfile(filepath="/tmp/my_first.blend", copy=False)
