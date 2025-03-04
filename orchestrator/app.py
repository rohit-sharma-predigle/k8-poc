from flask import Flask, jsonify, request
import json
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

@app.route('/run-job', methods=['POST'])
def run_job():
    """
    Endpoint to trigger a Kubernetes Job based on the job_specs JSON.
    """
    try:
        # Create the job in the default namespace
        resp = batch_v1.create_namespaced_job(
            body=job_specs,
            namespace="default"
        )
        return jsonify({
            "message": "Job created successfully",
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
