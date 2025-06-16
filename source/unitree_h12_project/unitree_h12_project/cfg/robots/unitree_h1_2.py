import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

H1_2_CFG = ArticulationCfg(
    prim_path="/World/envs/env_.*/Robot",
    spawn=sim_utils.UsdFileCfg(
        usd_path="/home/jiawen/unitree_h12_project/source/unitree_h12_project/unitree_h12_project/assets/robots/h1_2/h1_2.usd",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=4,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 1.05),
        joint_pos={".*joint": 0.0},
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*hip_yaw_joint", ".*hip_roll_joint", ".*hip_pitch_joint", ".*knee_joint", "torso_joint"
            ],
            effort_limit_sim=300,
            velocity_limit_sim=100.0,
            stiffness={".*": 200.0},
            damping={".*": 5.0},
        ),
        "feet": ImplicitActuatorCfg(
            joint_names_expr=[".*ankle_pitch_joint", ".*ankle_roll_joint"],
            effort_limit_sim=100,
            velocity_limit_sim=100.0,
            stiffness={".*": 20.0},
            damping={".*": 4.0},
        ),
        "arms": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*shoulder_pitch_joint", ".*shoulder_roll_joint", ".*shoulder_yaw_joint",
                ".*elbow_pitch_joint", ".*elbow_roll_joint"
            ],
            effort_limit_sim=300,
            velocity_limit_sim=100.0,
            stiffness={".*": 40.0},
            damping={".*": 10.0},
        ),
        # 你可以视任务是否加上手指控制
        # "hands": ImplicitActuatorCfg(
        #     joint_names_expr=[".*_joint"],  # 或匹配特定 L_index、R_thumb 等
        #     effort_limit_sim=50,
        #     velocity_limit_sim=30.0,
        #     stiffness={".*": 5.0},
        #     damping={".*": 1.0},
        # ),
    },
)

