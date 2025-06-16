# Unitree H1-2 项目开发日志（IsaacLab）

**日期：** 2025-06-16  
**作者：** jiawen  
**项目路径：** `/home/jiawen/unitree_h12_project`  
**机器人：** Unitree H1-2  
**仿真平台：** IsaacLab (基于 Isaac Sim)

---

## 📦 项目初始化

- 使用 `./isaaclab.sh --new` 创建了名为 `unitree_h12_project` 的外部项目。
- 项目结构遵循模板生成，扩展目录位于 `source/unitree_h12_project/unitree_h12_project/tasks/direct/unitree_h12_project/`。
- 成功列出模板任务 `UnitreeH12Task-v0`。

---

## 🤖 H1-2 模型导入与封装

- 使用 URDF Import Extension 将 `/home/jiawen/workspace/unitree_rl/unitree_rl_gym/resources/robots/h1_2/h1_2.urdf` 转换为 USD 文件。
- 输出路径：`unitree_h12_project/assets/robots/h1_2/h1_2.usd` 以及 `configuration/` 文件夹（包含 sensor/physics 子文件）。
- `ArticulationCfg` 被封装为 `H1_2_CFG`，设定初始姿态与 actuator 配置。

---

## 🧠 环境任务创建与适配

### Task 文件

- 移除了模板中的 cartpole 残留字段，如 `slider_to_cart`, `cart_dof_name` 等。
- 基于 `DirectRLEnv` 重构了 `unitree_h12_task.py` 和 `unitree_h12_task_cfg.py`：
  - 使用 `Articulation` 加载 H1-2；
  - `_apply_action()` 实现为 `set_joint_position_target()`；
  - `_get_observations()` 拼接 `joint_pos + joint_vel`；
  - `_get_rewards()` 使用简单的高度维持逻辑；
  - `_get_dones()` 检测机器人是否倒下或超时。

### Action/Observation 空间

- 通过打印 `self.robot.joint_names`，确定总 DOF 数为 51；
- 配置文件更新：
  ```python
  action_space = 51
  observation_space = 102
  ```

---

## 🧪 调试过程与问题排查

### ✅ 已解决问题

- `gymnasium.error.NameNotFound` → task 注册名拼写不一致，已修复为 `Unitree_H12Task-v0`
- `ImportError: cannot import name 'ImplicitActuatorCfg'` → 替换为正确模块路径
- `ModuleNotFoundError: 'isaaclab.sim.physx'` → 使用 `RigidBodyPropertiesCfg` 等路径替代
- USD 文件路径错误 → 使用 `relative_path` or 绝对路径修复
- `"Not all regular expressions are matched!"` → 更新 actuators 中正则为实际关节名
- `AttributeError: 'Articulation' object has no attribute 'actuated_dof_indices'` → 使用 `range(N)` 临时替代

### ⚠️ 典型警告

- `effort_limit` 与 `velocity_limit` 参数将被弃用 → 建议改为 `effort_limit_sim`, `velocity_limit_sim`
- `"Not all actuators are configured"` → 当前 actuator 仅覆盖部分 joints（23/51）

---

## 🪄 工具与技巧

- 使用 `print(self.robot.joint_names)` 确定 USD 模型中关节命名
- 模拟动作时只控制 actuated joints，避免维度 mismatch
- 将打印语句放在 `_reset_idx()` 内避免过早访问未初始化对象

---

## 📌 后续建议

- 明确哪些关节需要控制，精确列出 actuator 名单并传入 joint_ids
- 编写 reward shaping 逻辑：如 energy、torso height、速度控制等
- 配置 PPO 训练脚本，如 `scripts/rsl_rl/train.py`
- 使用 motion imitation (AMP) 进行进一步研究

---

