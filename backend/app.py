from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os

from railway import (
    list_projects,
    list_services,
    service_logs,
    service_metrics,
    start_service,
    stop_service,
    redeploy_service
)

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

ADMIN_USER = "dev"
ADMIN_PASS = "dev@123"

@app.post("/api/login")
def login():
    data = request.json
    if data["username"] == ADMIN_USER and data["password"] == ADMIN_PASS:
        return {"token": create_access_token(identity="admin")}
    return {"error": "invalid"}, 401

@app.get("/api/projects")
@jwt_required()
def projects():
    return jsonify(list_projects())

@app.get("/api/services/<project_id>")
@jwt_required()
def services(project_id):
    return jsonify(list_services(project_id))

@app.get("/api/logs/<service_id>")
@jwt_required()
def logs(service_id):
    return jsonify(service_logs(service_id))

@app.get("/api/metrics/<service_id>")
@jwt_required()
def metrics(service_id):
    return jsonify(service_metrics(service_id))

@app.post("/api/action")
@jwt_required()
def action():
    d = request.json
    if d["action"] == "start":
        start_service(d["service_id"])
    elif d["action"] == "stop":
        stop_service(d["service_id"])
    elif d["action"] == "redeploy":
        redeploy_service(d["service_id"])
    return {"status": "ok"}

app.run(host="0.0.0.0", port=5000)
