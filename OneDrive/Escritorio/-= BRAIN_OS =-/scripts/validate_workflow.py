import yaml
import sys

workflow_path = r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\.github\workflows\deploy-medioevo-tools.yml"

try:
    with open(workflow_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    print("YAML válido")
    print("Jobs:", list(data.get('jobs', {}).keys()))
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)