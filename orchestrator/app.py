from flask import Flask, jsonify, request
import json
import datetime
from kubernetes import client, config

app = Flask(__name__)

# Load job specs from the JSON file
with open('job_specs.json') as f:
    job_specs = json.load(f)

# Configure the Kubernetes client
try:
    # Use in-cluster configuration when running inside Kubernetes
    config.load_incluster_config()
except Exception:
    # Fallback to kubeconfig when running locally
    config.load_kube_config()

batch_v1 = client.BatchV1Api()

@app.route('/run-job/<job_name>', methods=['POST'])
def run_job(job_name):
    # Check if the requested job exists in the specs
    if job_name not in job_specs:
        return jsonify({"error": f"Job spec for '{job_name}' not found"}), 404

    job_spec = job_specs[job_name]

    # Append a timestamp to the job name to ensure uniqueness
    unique_suffix = int(datetime.datetime.now().timestamp())
    original_name = job_spec['metadata']['name']
    unique_job_name = f"{original_name}-{unique_suffix}"
    job_spec['metadata']['name'] = unique_job_name
    job_spec['spec']['template']['metadata']['name'] = unique_job_name

    try:
        # Create the job in the "default" namespace
        resp = batch_v1.create_namespaced_job(
            body=job_spec,
            namespace="default"
        )
        return jsonify({
            "message": f"Job '{job_name}' triggered successfully",
            "job_name": resp.metadata.name
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "Flask Kubernetes Job Runner is up and running!"


if __name__ == '__main__':
    # Listen on all interfaces on port 5000
    app.run(host='0.0.0.0', port=5000)
