# Docker Compose Local Development Port Mapper

A simple yet powerful solution to streamline local development while keeping heavy services on remote servers. This project creates lightweight Docker proxy images that forward traffic to remote services via SSH. Ideal for scenarios where you want to develop locally but use resource-intensive services like databases, ELK stacks, or other backend services hosted remotely.

## 🚀 Overview

This tool solves a common challenge in microservices development: the need to have instant **feedback loop** and run **resource-intensive services** locally at the same time. Instead of running heavy services like ELK Stack, databases, or machine learning models on your development machine, this tool creates lightweight proxy containers that forward traffic to the actual services running on a remote server.

## 🔑 Key Benefits

- 🔥 Dramatically reduced local resource usage.
- 🚄 Faster local development setup and ⚡️ instant feedback loop.
- 💻 Work with production-like environments locally (mostly **staging** environments).
- 🔒 Secure SSH-based communication.
- 🔌 Seamless integration with existing docker compose files.

## 🛠 How It Works

The tool creates a proxy Docker image that replaces the actual service image in your local docker compose file.

When the proxy container starts, it:

- Establishes an SSH connection to the remote server.
- Identifies the target service container on the remote server.
- Sets up port forwarding from your local machine to the remote container.
- Maintains the SSH connection for the duration of the container's life.

## 📋 Prerequisites

- Docker and Docker Compose installed locally.
- SSH access to the remote server.
- Docker and Docker Compose running on the remote server.

## 🔧 Installation

1. Clone this repository:

```bash
git clone https://github.com/amhoba2014/docker-compose-local-development-port-mapper
cd docker-compose-local-development-port-mapper
```

2. Generate and copy your SSH key:

```bash
cp /path/to/your/existing/ssh/key ./assets/ssh_key
```

3. Set proper permissions:

```bash
chmod 600 ./assets/ssh_key
```

4. Configure your remote server settings:

- `REMOTE_USER`: Username of the remote server that SSH key is created for.
- `REMOTE_IP`: IP address of the remote server.
- `REMOTE_PATH`: Path on the remote server to the directory containing the *docker-compose.yml*.
- `REMOTE_BASE_COMPOSE_COMMAND`: The base *docker compose* command that is used on remote server to spin up containers.

```bash
nano ./assets/configuration.py
```

## 📝 Usage

1. Build the image:

```bash
cd docker-compose-local-development-port-mapper
bash build.sh
```

2. Modify your local `docker-compose.yml`:

Replace the original service images with the port mapper image:

```yaml
services:
  heavy_service:
    image: port_mapper:latest
    environment:
      - SERVICE_NAME=heavy_service
      - SERVICE_PORT=8080
```

3. Start your development environment:

```bash
docker compose up
```

## 🌟 Example

Converting an ELK stack service to use port mapping:

### Original service:

This is part of a bigger `docker-compose.yml` file running on a **dev** or **staging** server.

```yaml
elasticsearch:
  build:
    context: ../elasticsearch
    target: dev
  ports:
    - "9200:9200"
```

### With port mapper:

This is part of our local `docker-compose.yml` file, shall run locally.

```yaml
elasticsearch:
  image: port_mapper:latest
  environment:
    - SERVICE_NAME=elasticsearch
    - SERVICE_PORT=9200
```

## 🔐 Security Considerations

1. Never commit SSH keys to version control and use this project locally and share it with colleagues over a trusted wire (USB drive or local network).
2. Use dedicated keys for the port mapper.
3. Regularly rotate SSH keys.

## 🚧 Limitations

- Works only with **docker compose** based setups (which I know most organisations do not use them in staging). Can be tweaked to support **Kubernetes** and **VPC** (GCP, AWS, Azure) based setups.
- A slight latency, dependent on the network connection type.
- Requires high speed and stable internet connection (optic fiber works best).

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

# 👏 Acknowledgments

Inspired by the need for efficient local development at my previous job.

This is more like a SRE/DevOps tooling and type of work, which I almost do most of the times for both myself and my colleagues.