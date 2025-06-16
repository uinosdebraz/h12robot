# 📘 Unitree H12 仿真开发日志

## 项目起始（目标）

构建一个基于 Isaac Lab 和 Omniverse Isaac Sim 的强化学习仿真平台，适配 Unitree H1.2 机器人模型，并最终实现可训练、推理及可复现的 Docker 环境。

---

## 🛠️ 环境配置与 VS Code 设置

### ✅ 使用 pip 安装 Isaac Sim：

```bash
pip install 'isaacsim[all,extscache]==4.5.0' --extra-index-url https://pypi.nvidia.com
```

### ✅ 安装 Isaac Lab 并初始化：

```bash
git clone git@github.com:isaac-sim/IsaacLab.git
cd IsaacLab
./isaaclab.sh --install
```

### ✅ 配置自己的新项目（unitree\_h12\_project）：

- 复制模板目录
- 修改 `extension.toml`
- 修改任务名为 `Unitree_H12Task-v0`

### ✅ VS Code 启动失败问题排查：

- 原因：环境中找不到 `python.sh`
- 解决方案：用 `python3 .vscode/tools/setup_vscode.py --isaac_path <路径>` 手动配置

---

## 🧪 强化学习调试过程

### ✅ 训练成功

- 使用 `train.py` 成功训练模型
- 设置 `num_envs = 256`（因显存仅 6GB）
- 模型输出路径：`logs/rsl_rl/cartpole_direct/`

### ✅ 推理阶段问题

- 遇到机器人未配置 actuator 报错（23 != 51）
- 警告信息保留但推理仍可执行

---

## 🐳 Docker 开发

### ✅ Dockerfile 编写与构建

- 文件名统一为 `Dockerfile`
- 使用 base image: `nvidia/cuda:12.2.0-devel-ubuntu22.04`
- 添加 miniconda 并构建 Conda 环境

### ⚠️ 安装报错记录

1. 找不到 `omniisaacgymenvs` → 移除该 pip 依赖
2. `rsl-rl` 本地路径格式错误：
   - 原：`./scripts/rsl_rl`
   - 改：`-e scripts/rsl_rl`
3. `unitree_h12_project` 安装失败：路径需指向真正模块所在
   - 使用：`-e source/unitree_h12_project`

### ✅ 构建命令

```bash
docker build -t h12robot .
```

---

## ☁️ Docker Hub 发布流程

### 登录 Docker Hub

```bash
docker login
```

### 打标签并推送

```bash
docker tag h12robot uinosdebraz/h12robot:latest
docker push uinosdebraz/h12robot:latest
```

### 运行测试容器

```bash
docker run -it --rm --gpus all -v $(pwd):/workspace -w /workspace h12robot
```

---

## ✅ GitHub 操作记录

- 项目仓库：https\://github.com/uinosdebraz/h12robot
- 常用命令：

```bash
git add .
git commit -m "Update for Docker support"
git push origin main
```

---

## ✅ 最终成果总结

- 成功构建自定义任务 `Unitree_H12Task-v0`
- 在低显存 GPU 上运行 256 环境训练
- 推理脚本可正常加载模型
- 项目成功打包为 Docker 镜像并发布
- 所有代码、依赖与训练模型已提交至 GitHub

---

## 📌 待改进

- 推理阶段对 actuator 的警告可进一步完善模型
- Docker 镜像大小优化
- 加入 wandb 可视化与日志上传支持

---

> 日志记录人：ChatGPT（Claude 3.5 Sonnet） + Jiawen @ 2025-06-16

