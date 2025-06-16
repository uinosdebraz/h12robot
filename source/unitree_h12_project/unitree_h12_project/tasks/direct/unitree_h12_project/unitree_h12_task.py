import torch
from isaaclab.sim import DomeLightCfg
from isaaclab.assets import Articulation
from isaaclab.envs import DirectRLEnv
from isaaclab.sim.spawners.from_files import GroundPlaneCfg, spawn_ground_plane
from .unitree_h12_task_cfg import UnitreeH12TaskCfg

class UnitreeH12Task(DirectRLEnv):
    cfg: UnitreeH12TaskCfg

    def __init__(self, cfg: UnitreeH12TaskCfg, render_mode=None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)

    def _setup_scene(self):
        self.robot = Articulation(self.cfg.robot_cfg)
        spawn_ground_plane("/World/ground", GroundPlaneCfg())
        self.scene.clone_environments()
        self.scene.articulations["robot"] = self.robot
        DomeLightCfg(intensity=2000.0).func("/World/Light", DomeLightCfg())
        
        # joint_names = self.robot.joint_names
        
        # 假设你的 actuator 中定义了 arms、legs、feet
        # actuated_joint_names = []
        # for actuator in self.robot.cfg.actuators.values():
            # for expr in actuator.joint_names_expr:
                # matched = [j for j in joint_names if torch.regex_match(j, expr)]
                # actuated_joint_names.extend(matched)

	# 去重并排序
        # actuated_joint_names = sorted(set(actuated_joint_names), key=joint_names.index)
        # print("Matched actuated joints:", actuated_joint_names)


    def _pre_physics_step(self, actions: torch.Tensor) -> None:
        self.actions = actions.clone()

    # def _apply_action(self) -> None:
        # 使用 ImplicitActuatorCfg 的 joint_position_target 控制方式
    	# self.robot.set_joint_position_target(
        	# self.actions * self.cfg.action_scale,
        	# joint_ids=self.robot.actuated_joint_indices,
    	# )	
    	
    def _apply_action(self) -> None:
        # 简化处理：假设动作对前 N 个关节生效
        joint_ids = list(range(self.actions.shape[1]))  # [0, 1, ..., N-1]
        self.robot.set_joint_position_target(self.actions * self.cfg.action_scale, joint_ids=joint_ids)

    def _get_observations(self) -> dict:
        obs = torch.cat(
            [self.robot.data.joint_pos, self.robot.data.joint_vel],
            dim=-1
        )
        return {"policy": obs}

    def _get_rewards(self) -> torch.Tensor:
        # 示例：站稳 + 不倒地
        base_height = self.robot.data.root_pos_w[:, 2]
        reward = (base_height > 0.8).float()  # 简单站立奖励
        return reward

    def _get_dones(self) -> tuple[torch.Tensor, torch.Tensor]:
        timeout = self.episode_length_buf >= self.max_episode_length - 1
        fallen = self.robot.data.root_pos_w[:, 2] < 0.4
        return fallen, timeout

    def _reset_idx(self, env_ids=None):
        if env_ids is None:
            env_ids = self.robot._ALL_INDICES
        self.robot.reset(env_ids)
        
        # print("All joints:", self.robot.joint_names)

        super()._reset_idx(env_ids)

