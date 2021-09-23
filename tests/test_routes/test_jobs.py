import json

def  test_create_job(client):
    data={
        "title" : "Title 1",
        "company" : "teste 2",
        "company_url" : "www.co.nz",
        "location" : "NZ",
        "description" : "Testing",
        "date_posted" : "2021-09-21"
        } 
    response = client.post("/jobs/create-job", json.dumps(data))
    assert response.status_code == 200

def test_retrive_job_by_id(client):
    data={
    "title" : "Sr Prod Mgr",
    "company" : "test 3",
    "company_url" : "www.co.nz",
    "location" : "NZ",
    "description" : "Testing",
    "date_posted" : "2021-09-21"
    } 
    client.post("/jobs/create-job", json.dumps(data))
    response = client.get("/jobs/get/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Sr Prod Mgr"

    response = client.get("/jobs/get/2")
    assert response.status_code == 404

    response = client.get("/jobs/get/a")
    assert response.status_code == 422