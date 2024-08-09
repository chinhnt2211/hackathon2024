from fastapi import FastAPI
from pydantic import BaseModel
import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime


app = FastAPI()

# -----------------------TEST------------------------------------
@app.get("/")
async def test():
    return {"message": "Hello World"}

# -----------------------API Get Detail--------------------------------

# -----------------------API Test connect------------------------------

# -----------------------API MIGRATE DATA------------------------------
class fdemigrate(BaseModel):
    username: str
    password: str
    host: str
    port: str
    org_name: str
    vdc_name: str
    cluster_id: str

@app.post("/migration/migrate")
async def migrate(item: fdemigrate):

    # CHECK: CONFIRM DATA
    print("Username: " + item.username)
    print("password: " + item.password)
    print("host: " + item.host)
    print("port: " + item.port)
    print("org_name: " + item.org_name)
    print("vdc_name: " + item.vdc_name)
    print("cluster_id: " + item.cluster_id)

    # GENERAL INFORMATION
    headers = {
        'Authorization': 'Bearer VCk1E7mNA8lTiSTRpaBIggotatZoSM',
        'Content-Type': 'application/json'
    }
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # STEP 1: COPY ORIGIN WORKFLOW TO A NEW WORKFLOW

    ## STEP 1.1: CALL API COPY WORKFLOW
    url_copy_workflow = 'https://awx-dev.fde.fptcloud.com/api/v2/workflow_job_templates/15404/copy/'
    data_copy_workflow = {
        "name": "Hackathon migrate to " + item.cluster_id + " " + current_time
    }
    response_copy_workflow = requests.post(url_copy_workflow, headers=headers, json=data_copy_workflow)

    ## STEP 1.2: SAVE NEW WORKFLOW ID
    new_workflow_id = response_copy_workflow.json()['id']

    # STEP 2: FIND INVENTORY

    ## STEP 2.1: CALL API GET INVENTORY
    url_get_inventory = 'https://awx-dev.fde.fptcloud.com/api/v2/inventories?search=' + item.cluster_id
    response_inventory = requests.get(url_get_inventory, headers=headers)

    ## STEP 2.2: SAVE INVENTORY ID
    inventory_id = response_inventory.json()['results'][0]['id']

    # STEP 3: LAUNCH WORKFLOW

    ## STEP 3.1: CALL API LAUNCH JOB
    url_launch_job = f'https://awx-dev.fde.fptcloud.com/api/v2/workflow_job_templates/{new_workflow_id}/launch/'
    data_launch_job = {
        "extra_vars": f"{{org_name: {item.org_name},vdc_name: {item.vdc_name},source_host: {item.host},source_port: {item.port},source_user: {item.username},source_pass: {item.password}}}",
        "inventory": inventory_id
    }

    response_launch_job = requests.post(url_launch_job, headers=headers, json=data_launch_job)

    ## STEP 3.2: SAVE WORKFLOW JOB ID
    workflow_job_id = response_launch_job.json()['workflow_job']

    # STEP 4: SAVE THE STATUS OF MIGRATION TO DATABASE
    connection = psycopg2.connect(
        host="103.160.75.63",
        database="DBdefault",
        user="admin",
        password="Pk32qrNW6LqD",
        port=15432
    )

    cursor = connection.cursor()

    cluster_id = item.cluster_id
    host = item.host
    port = item.port
    username = item.username
    password = item.password
    status = 'processing'
    workflow_id = workflow_job_id
    migrate_at = current_time

    insert_query = sql.SQL("""
        INSERT INTO migration (cluster_id, host, port, username, password, status, workflow_id, migrate_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """)

    cursor.execute(insert_query, (cluster_id, host, port, username, password, status, workflow_id, migrate_at))
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Success",
            "data": {
                "Successed": True
            }
            }