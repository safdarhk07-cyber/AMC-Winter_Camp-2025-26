import pybullet as p
import pybullet_data
import time
import math

# Initialize Simulation
p.connect(p.GUI)  
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")
p.setGravity(0, 0, -10)

#Ramp Formation
def create_ramp():
    # Dimensions
    length = 10
    width = 5
    thickness = 0.2
    
    # Create a Box Shape
    # halfExtents are [length/2, width/2, height/2]
    col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[length/2, width/2, thickness/2])
    vis_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[length/2, width/2, thickness/2], rgbaColor=[0.7, 0.5, 0.3, 1])

    # Position: Placed ahead of the Husky
    # Orientation: Tilted up by ~15 degrees (0.26 radians)
    ramp_angle = -0.26 
    start_pos = [-5, 0, 1.3] # Approximate center position to make the ramp start near x=3
    ramp_orn = p.getQuaternionFromEuler([0, -ramp_angle, 0])

    # Create the Body (Mass=0 makes it static/immovable)
    ramp_id = p.createMultiBody(baseMass=0, 
                                baseCollisionShapeIndex=col_shape, 
                                baseVisualShapeIndex=vis_shape, 
                                basePosition=start_pos, 
                                baseOrientation=ramp_orn)
    
    # Set Friction so the robot can climb
    p.changeDynamics(ramp_id, -1, lateralFriction=0.9)
    return ramp_id

# Create the ramp
ramp = create_ramp()

# Load Husky
huskypos = [3, 0, 0.1]
husky = p.loadURDF("husky/husky.urdf", huskypos[0], huskypos[1], huskypos[2])


# --- 2. Identify Wheels ---
num_joints = p.getNumJoints(husky)
wheel_indices = []

print("------------------------------------------------")
print(f"Total Joints: {num_joints}")
for i in range(num_joints):
    joint_info = p.getJointInfo(husky, i)
    name = joint_info[1].decode('utf-8')
    if "wheel" in name or "joint" in name:
        # 2, 3, 4, 5 are usually the wheels on the standard husky URDF
        if joint_info[2] == p.JOINT_REVOLUTE:
            wheel_indices.append(i)
print(f"Wheel Indices found: {wheel_indices}")
print("------------------------------------------------")


# --- 3. User Menu ---
print("\nSelect Control Mode:")
print("1. Torque Control (Enter 't')")
print("2. Velocity Control (Enter 'v')")
# Default to velocity if input fails (for safety)
try:
    mode = input("Enter choice: ").strip().lower()
except:
    mode = 'v'


# --- 4. Control Functions ---

def Torque_control():
    # Tuned value: 60-80Nm is often needed for a steep ramp
    optimal_torque_value = 80 
    
    # CRITICAL: Disable velocity motor to allow torque control
    p.setJointMotorControlArray(husky, wheel_indices, p.VELOCITY_CONTROL, forces=[0]*len(wheel_indices))
    
    # Apply Torque
    for joint_index in wheel_indices:
        p.setJointMotorControl2(
            bodyUniqueId=husky, 
            jointIndex=joint_index, 
            controlMode=p.TORQUE_CONTROL, 
            force=optimal_torque_value
        )

def Velocity_control():
    maxForce = 200 # High force limit to ensure it can push up the hill
    optimal_velocity_value = -100 # Rad/s
    
    for joint_index in wheel_indices:
        p.setJointMotorControl2(
            bodyUniqueId=husky, 
            jointIndex=joint_index, 
            controlMode=p.VELOCITY_CONTROL, 
            targetVelocity=optimal_velocity_value,
            force=maxForce
        )


# --- 5. Main Loop ---
step_counter = 0

while (1):
    time.sleep(1./960.)
    
    if mode == 't':
        Torque_control()
    else:
        Velocity_control()
    
    p.stepSimulation()
    step_counter += 1

    # Print status every 100 steps
    if step_counter % 100 == 0:
        pos, _ = p.getBasePositionAndOrientation(husky)
        lin_vel, _ = p.getBaseVelocity(husky)
        speed = (lin_vel[0]**2 + lin_vel[1]**2 + lin_vel[2]**2)**0.5
        
        print(f"Step {step_counter} | Height: {pos[2]:.2f}m | Speed: {speed:.2f} m/s")

p.disconnect()