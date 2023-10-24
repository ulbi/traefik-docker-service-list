# Traefik - Docker Service lister

## Overview

The goal of this project is to create a simple, yet effectively formatted web application to display all Docker services that are proxied by Traefik. Built with Flask and Bootstrap, the application interfaces with the Docker API to provide real-time information on running services. 

### Features

- Automatically fetches and displays services running under Docker, which are proxied by Traefik.
- Assigns distinct background colors to different service stacks.
- Allows users to add a description to each service by setting a service label `service.<label>.description`.

## Prerequisites

- Docker
- Python 3.x (if running outside of Docker)

## Development Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. Navigate to the project directory:
    ```bash
    cd yourrepository
    ```

3. Build the Docker image:
    ```bash
    docker build -t your_image_name .
    ```

4. Run the Docker container:
    ```bash
    docker run -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock your_image_name
    ```

    **Optional: You can also set environment variables:**

    ```bash
    docker run -e DOCKER_BASE_URL='unix:///var/run/docker.sock' \
               -e EXCLUSIONS='/api/v1/admin,auth.sampledomain.com' \
               -e HOST='0.0.0.0' \
               -e PORT='5000' \
               -e LOG_LEVEL='INFO' \
               -e DOMAIN='.sampledomain.com' \
               -p 5000:5000 \
               -v /var/run/docker.sock:/var/run/docker.sock \
               your_image_name
    ```

5. Open your browser and navigate to [http://localhost:5000](http://localhost:5000)

## Environment Variables

- `DOCKER_BASE_URL`: Docker API URL
- `EXCLUSIONS`: Comma-separated list of exclusions for Traefik routes
- `HOST`: Host for Flask to bind to
- `PORT`: Port for Flask to bind to
- `LOG_LEVEL`: Logging level (e.g., 'INFO', 'DEBUG')
- `DOMAIN`: Domain suffix for services

## License

[MIT License](LICENSE.md)
