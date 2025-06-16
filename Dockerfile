# Use official CUDA base image with Python
FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget git curl ca-certificates bzip2 build-essential libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
ENV CONDA_DIR=/opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p $CONDA_DIR && \
    rm ~/miniconda.sh
ENV PATH=$CONDA_DIR/bin:$PATH

# Create conda environment and install dependencies
COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && conda clean -a -y

# Activate environment
SHELL ["/bin/bash", "-c"]
RUN echo "conda activate env_isaaclab" >> ~/.bashrc
ENV CONDA_DEFAULT_ENV=env_isaaclab
ENV PATH /opt/conda/envs/env_isaaclab/bin:$PATH

# Set working directory
WORKDIR /workspace/h12robot

# Copy project files
COPY . /workspace/h12robot

# Set default command to run training (can override in docker run)
CMD ["python", "scripts/rsl_rl/train.py", "--task", "Unitree_H12Task-v0", "--num_envs", "256", "--headless"]
