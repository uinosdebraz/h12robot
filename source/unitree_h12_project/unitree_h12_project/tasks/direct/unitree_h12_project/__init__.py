# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import gymnasium as gym

from . import agents

##
# Register Gym environments.
##


gym.register(
    id="Unitree_H12Task-v0",
    entry_point=f"{__name__}.unitree_h12_task:UnitreeH12Task",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.unitree_h12_task_cfg:UnitreeH12TaskCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:PPORunnerCfg",
    },
)
