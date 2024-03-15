# Time interval is 1/1000 of a second

# Approximate the torque in Nm using current % velocity

def torqueCalculate(rpm, maxRPM, motors):
    cartridgeMultiplier = 100/maxRPM

    if rpm < 59.5:
        return cartridgeMultiplier*(-0.002*rpm + 2.15)*motors
    else:
        return cartridgeMultiplier*(-0.0335*(rpm-59.5)+2.03)*motors


# Drivetrain Combinations [cartridge, gearRatio (driving/driven), diameter, motors]
# combinations = [[600, 60/60, 2.75, 6], [600, 60/60, 2.75, 4],
#                 [600, 36/60, 3.75, 6], [600, 48/72, 3.25, 4], [600, 36/48, 2.75, 6]]
combinations = [[600, 36/60, 3.25, 6], [600, 36/48, 3.25, 6], [600, 48/72, 3.25, 6], [600, 48/60, 3.25, 6], [600, 60/60, 2.75, 6], [600, 60/60, 3.25, 6]]

# Specify the distance you want to cover in inches
measureDistance = 24

# Specify the mass you want your combinations to drive with in kilograms
mass = 4
print(f"Time to pass {measureDistance} inches with mass of {mass}kg")

for i in range(0, len(combinations)):
    # Drivetrain constants
    gearRatio = combinations[i][1]  # driving/driven
    cartridge = combinations[i][0]

    # Diameter in inches
    radius = combinations[i][2]/2

    # Calculate Max RPM and max linear speed using constants
    maxRPM = cartridge*gearRatio
    maxLinearSpeed = radius*2*3.14159 * (maxRPM/60)

    # Telemetry variables
    time = 0
    distance = 0
    percentSpeed = 0
    linearSpeed = 0

    # Continue until the robot reaches a distance of 144 inches
    while distance < measureDistance:
        # Calculate current torque
        torque = torqueCalculate(percentSpeed, maxRPM, combinations[i][3])

        # Calculate the force in Newtons
        force = torque/(radius/39.37)

        # Calculate the acceleration in m/s^2. Convert it to in/s^2 and divide by 1000000 to adjust for time interval (1/1000 of second)
        acceleration = ((force/mass)*39.37)/1000000

        # Add speed to acceleration
        linearSpeed += acceleration

        # Limit the speed as the motor reaches 100%
        if linearSpeed*1000 > maxLinearSpeed:
            linearSpeed = maxLinearSpeed/1000

        # Add the speed to the distance
        distance += linearSpeed

        # Calculate percent speed for torque calculation
        percentSpeed = (linearSpeed/(maxLinearSpeed/1000))

        # Adjust the time
        time += 1

    print(
        f'Diameter: {radius*2}", RPM: {round(maxRPM)}, Motors: {combinations[i][3]}, Mass: {mass}kg | Time: {time/1000}s')
