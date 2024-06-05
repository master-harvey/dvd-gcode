def generate_gcode_with_solenoid(width, height, start_x, start_y, vx, vy, num_steps, corner_threshold=5):
    gcode = []
    gcode.append("G21 ; Set units to millimeters")
    gcode.append(f"G0 X{start_x:.2f} Y{start_y:.2f} ; Move to start position")
    
    x, y = start_x, start_y
    solenoid_on = False
    
    for _ in range(num_steps):
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
    
    # Ensure solenoid is off at the end of the program
    gcode.append("M42 P0 S0 ; Turn off solenoid at end")
    
    return gcode

# CNC machine parameters
width = 2684  # mm
height = 1352  # mm
start_x = width / 2
start_y = 0
vx = 0.2  # mm per step
vy = 0.2  # mm per step
num_steps = 200000

# Generate G-code
gcode = generate_gcode_with_solenoid(width, height, start_x, start_y, vx, vy, num_steps)

# Print the G-code
for line in gcode:
    print(line)