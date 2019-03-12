import subprocess
from flask import (Flask, request, abort)

app = Flask(__name__)  # create the application instance


@app.route('/welder/api/syncTo', methods=['POST'])
def sync_to():
    if not request or 'destination' not in request.json:
        abort(400)
    destination = request.json['destination']
    if not validate_bucket(destination):
        return "destination {0} is not a valid GCS bucket".format(destination), 400
    command = ['gsutil', '-m', 'rsync', '-r', '/Users/vkumra/Documents/interviews', destination]
    run_command(command)
    return "Accepted", 202


@app.route('/welder/api/syncFrom', methods=['POST'])
def sync_from():
    if not request or 'source' not in request.json:
        abort(400)
    source = request.json['source']
    if not validate_bucket(source):
        return 'source {0} is not a valid GCS bucket'.format(source), 400
    command = ['gsutil', '-m', 'rsync', '-r', source, '/Users/vkumra/Documents/interviews']
    run_command(command)
    return "Accepted", 202


def validate_bucket(bucket_name):
    bucket_name.startswith("gs://")


def run_command(command):
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
