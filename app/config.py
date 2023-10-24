# Configuration for Flask app
import os

# Load environment variables
DOCKER_BASE_URL = os.getenv('DOCKER_BASE_URL', 'unix:///var/run/docker.sock')
EXCLUSIONS = os.getenv('EXCLUSIONS', "/api/v1/admin,auth.sampledomain.com").split(',')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
DOMAIN = os.getenv('DOMAIN', '.sampledomain.com')