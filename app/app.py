from flask import Flask, render_template
from docker import DockerClient
import logging
import fnmatch
from hashlib import md5
import config

app = Flask(__name__)

app.config.from_object('config')
logging.basicConfig(level=app.config['LOG_LEVEL'])

def get_docker_client():
    return DockerClient(base_url=app.config['DOCKER_BASE_URL'])

def get_contrast_color(background_color):
    r, g, b = int(background_color[1:3], 16), int(background_color[3:5], 16), int(background_color[5:7], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return "#FFFFFF" if brightness < 128 else "#000000"

def get_color_from_string(input_string):
    return '#' + md5(input_string.encode()).hexdigest()[:6]

def process_services(client, exclusions, domain):
    services = client.services.list()
    stacks = {}
    for service in services:
        service_attrs = service.attrs
        stack_name = service_attrs['Spec']['Labels'].get('com.docker.stack.namespace', 'No Stack')
        logging.info(f"Processing service {service_attrs['Spec']['Name']} in stack {stack_name}")

        for label_key, label_value in service_attrs['Spec']['Labels'].items():
            if fnmatch.fnmatch(label_key, 'traefik.http.routers.*.rule'):
                traefik_rule = label_value

                if any(substring in traefik_rule for substring in exclusions):
                    logging.info(f"Skipping service {service_attrs['Spec']['Name']} due to filter")
                    continue
                    
                short_name = traefik_rule.split('`')[1].split('.')[0]
                description_key = f'service.{short_name}.description'
                description = service_attrs['Spec']['Labels'].get(description_key, '')                    
                logging.info(f"Load {description_key}")
                
                hostname = traefik_rule.split('`')[1]
                
                entry = {
                    'service_label': f"{hostname.replace(domain, '')}",
                    'url': f"https://{hostname}",
                    'description': description if description else f"Description for {description_key} is missing"
                }

                if stack_name not in stacks:
                    stacks[stack_name] = []
                stacks[stack_name].append(entry)
                
    stacks = {k: v for k, v in stacks.items() if v}
    return {k: sorted(v, key=lambda x: x['service_label']) for k, v in sorted(stacks.items())}

@app.route('/')
def index():
    try:
        logging.info("Fetching Docker API data...")
        client = get_docker_client()
        sorted_stacks = process_services(client, app.config['EXCLUSIONS'], app.config['DOMAIN'])
        logging.info("Rendering template...")
        return render_template('index.html', stacks=sorted_stacks, get_contrast_color=get_contrast_color, get_color_from_string=get_color_from_string)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return "An error occurred.", 500

def main():
    app.run(host=app.config['HOST'], port=app.config['PORT'])

if __name__ == '__main__':
    main()
