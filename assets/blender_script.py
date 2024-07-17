
import bpy
from math import radians, cos, sin

# Chemin du dossier où les images seront enregistrées
output_path = "/Users/monkeyparadise/Desktop/renders/"

# Noms des fichiers pour les rendus
filenames = ["render_0.png", "render_90.png", "render_180.png", "render_270.png"]

# Place the 3D cursor at the desired position
bpy.context.scene.cursor.location = (0, 0, 0)  # Modify this if needed

# Select the camera
camera = bpy.context.scene.camera
camera = bpy.data.objects.get("GameIsoCam")
if camera is None:
    raise ValueError("La caméra nommée 'GameIsoCam' n'a pas été trouvée.")
    

# Set the camera pivot to the 3D cursor
bpy.ops.object.select_all(action='DESELECT')
camera.select_set(True)
bpy.context.view_layer.objects.active = camera
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

# Function to rotate the camera
def rotate_camera(degrees):
    bpy.ops.transform.rotate(value=radians(degrees), orient_axis='Z', orient_type='CURSOR')

def render_image(output_file):
    bpy.context.scene.render.filepath = output_file
    bpy.ops.render.render(write_still=True)
    
def rotate_camera_around_cursor(camera, cursor, degrees):
    angle = radians(degrees)
    
    # Get current camera location
    cam_location = camera.location
    
    # Get cursor location
    cursor_location = cursor.location
    
    # Calculate the new location
    new_x = cos(angle) * (cam_location.x - cursor_location.x) - sin(angle) * (cam_location.y - cursor_location.y) + cursor_location.x
    new_y = sin(angle) * (cam_location.x - cursor_location.x) + cos(angle) * (cam_location.y - cursor_location.y) + cursor_location.y
    new_z = cam_location.z  # Z coordinate remains the same

    # Set the new location
    camera.location = (new_x, new_y, new_z)

    # Rotate the camera to look at the 3D cursor
    direction = cursor_location - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    
# Perform the rotations
for i, filename in enumerate(filenames):

    render_image(output_path + filename)
    print(f"Image rendue et enregistrée sous : {output_path + filename}")
    
    angle = 90
    cursor = bpy.context.scene.cursor
    rotate_camera_around_cursor(camera, cursor, angle)


# Restore original camera pivot if needed
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
print("Rendu complet.")
