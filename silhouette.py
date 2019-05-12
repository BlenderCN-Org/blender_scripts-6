import bpy
import bmesh
from mathutils import Vector

def draw_line(gp_frame, p0: tuple, p1: tuple):
    gp_stroke = gp_frame.strokes.new()
    gp_stroke.display_mode = '3DSPACE'
    
    # def geometry
    gp_stroke.points.add(count=2)
    gp_stroke.points[0].co = p0
    gp_stroke.points[1].co = p1
    return gp_stroke

bpy.ops.object.gpencil_add(view_align=False, location=(0, 0, 0), type='EMPTY')
gpencil = bpy.context.scene.objects[-1]
gpencil.name = "Silhouette"

gp_layer = gpencil.data.layers.new("Silhouette", set_active=True)

gp_frame = gp_layer.frames.new(0)

cam = bpy.data.objects.get("Camera")
cam_direction = cam.matrix_local.to_quaternion() @ Vector((0.0, 0.0, -1.0))

#gpencil.rotation_euler = cam.rotation_euler

cube = bpy.data.objects.get("Cube")
me = cube.data
bm = bmesh.new()
bm.from_mesh(me)

for edge in bm.edges:
    linked_faces = edge.link_faces
    if len(linked_faces) > 1:
        if (cam_direction @ linked_faces[0].normal) * (cam_direction @ linked_faces[1].normal) < 0:
            t0 = (edge.verts[0].co[0], edge.verts[0].co[1], edge.verts[0].co[2])
            t1 = (edge.verts[1].co[0], edge.verts[1].co[1], edge.verts[1].co[2])
            print(t0, t1)
            draw_line(gp_frame, t0, t1)
