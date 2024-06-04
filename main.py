import boto3
import os

def upload_to_s3(file_name, bucket_name, object_name=None):
    s3_client = boto3.client('s3')
    if object_name is None:
        object_name = file_name
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
    except Exception as e:
        print(f"Failed to upload {file_name} to S3: {e}")
        return False
    return True

def generate_gcode_with_solenoid(width, height, start_x, start_y, vx, vy, corner_threshold=5, lines_per_file=5000):
    gcode = []
    gcode.append("G21 ; Set units to millimeters")
    gcode.append(f"G0 X{start_x:.2f} Y{start_y:.2f} ; Move to start position")
    
    x, y = start_x, start_y
    solenoid_on = False
    file_counter = 0
    line_counter = 0

    while True:
        # Calculate the next position
        x_new = x + vx
        y_new = y + vy
        
        # Check for boundary collisions and adjust velocities
        if x_new <= 0 or x_new >= width:
            vx = -vx
        if y_new <= 0 or y_new >= height:
            vy = -vy
        
        # Update position based on adjusted velocities
        x += vx
        y += vy
        
        # Ensure the new position is within boundaries
        x = max(0, min(width, x))
        y = max(0, min(height, y))
        
        # Check if the end effector is within 5mm of a corner
        if ((x <= corner_threshold and y <= corner_threshold) or
            (x >= width - corner_threshold and y <= corner_threshold) or
            (x <= corner_threshold and y >= height - corner_threshold) or
            (x >= width - corner_threshold and y >= height - corner_threshold)):
            if(not solenoid_on):
                gcode.append("M42 P0 S255 ; Turn on solenoid")
                solenoid_on = True
        else:
            if(solenoid_on):
                gcode.append("M42 P0 S0 ; Turn off solenoid")
                solenoid_on = False
        
        # Generate G-code for the move
        gcode.append(f"G1 X{x:.2f} Y{y:.2f}")
        line_counter += 1
        
        # Save to file every lines_per_file lines
        if line_counter >= lines_per_file:
            file_name = f"gcode_part_{file_counter}.gcode"
            with open(file_name, 'w') as file:
                file.write("\n".join(gcode))
            
            # Upload to S3
            uploaded = upload_to_s3(file_name, os.environ['BUCKETNAME'], file_name)
            if uploaded:
                print(f"Uploaded {file_name} to S3")
                os.remove(file_name)
            
            # Reset gcode list and counters
            gcode = []
            file_counter += 1
            line_counter = 0

# CNC machine parameters
width = 3200  # mm
height = 1400  # mm
start_x = width / 2
start_y = 0
vx = 0.2  # 40mm/rotation? * 1/200 rotations/step = mm per step
vy = 0.2

# Generate G-code
generate_gcode_with_solenoid(width, height, start_x, start_y, vx, vy)
