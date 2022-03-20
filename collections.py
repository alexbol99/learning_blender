import bpy

bpy.data.collections.new('Suzannes')

coll_from = bpy.data.collections['Collection']
coll_to = bpy.data.collections['Suzannes']

to_unlink = []

for ob in coll_from.objects:
    try:
        coll_to.objects.link(ob)
    except RuntimeError:
        pass
    to_unlink.append(ob)
    
    
for ob in to_unlink:
    coll_from.objects.unlink(ob)
    
    
bpy.data.collections.remove(coll_from)

