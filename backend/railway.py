import requests, os

API = "https://backboard.railway.app/graphql"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('RAILWAY_API_KEY')}",
    "Content-Type": "application/json"
}

def gql(q, v=None):
    return requests.post(API, json={"query": q, "variables": v or {}}, headers=HEADERS).json()

def list_projects():
    return gql("""{ projects { edges { node { id name }}}}""")

def list_services(pid):
    return gql("""
    query($id:ID!){
      project(id:$id){
        services{edges{node{id name}}}
      }
    }""", {"id": pid})

def service_logs(sid):
    return gql("""
    query($id:ID!){
      service(id:$id){
        logs(limit:100)
      }
    }""", {"id": sid})

def service_metrics(sid):
    return gql("""
    query($id:ID!){
      service(id:$id){
        metrics{cpu memory}
      }
    }""", {"id": sid})

def start_service(sid):
    gql("mutation($id:ID!){serviceScale(serviceId:$id,replicas:1){id}}",{"id":sid})

def stop_service(sid):
    gql("mutation($id:ID!){serviceScale(serviceId:$id,replicas:0){id}}",{"id":sid})

def redeploy_service(sid):
    gql("mutation($id:ID!){serviceRedeploy(serviceId:$id){id}}",{"id":sid})
