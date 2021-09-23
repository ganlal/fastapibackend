import json

def test_create_job(client,normal_user_token_headers):   #added normal_user_token_headers
    data = {
        "title": "SDE super",
        "company": "doogle",
        "company_url": "www.doogle.com",
        "location": "USA,NY",
        "description": "python",
        "date_posted": "2022-03-20",
    }
    response = client.post("/jobs/create-job/",data=json.dumps(data),headers=normal_user_token_headers)  #added header in the post request
    assert response.status_code == 200
    assert response.json()["company"] == "doogle"
    assert response.json()["description"] == "python"

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