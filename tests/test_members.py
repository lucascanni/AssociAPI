from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_member_success(auth_user):
    res = client.post("/members",headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
        }, json={
            "nom": "canni",
            "prenom": "lucas",
            "email": "l@gmail.com",
            "telephone": "0607080900",
        }
    )
    assert res.status_code == 201

def test_create_member_unauthorized():
    res = client.post("/members", json={
        "nom": "canni",
        "prenom": "lucas",
        "email": "l@gmail.com",
        "telephone": "0607080900"
    })
    assert res.status_code == 401

def test_get_all_members(auth_user):    
    res = client.get("/members", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert res.status_code == 200

def test_get_member_by_id(auth_user, create_member):
    res = client.get("/members/{create_member['id']}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert res.status_code == 200

def test_get_member_by_id_not_found(auth_user):
    res = client.get("/members/2", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert res.status_code == 404

def test_update_member(auth_user):
    res= client.patch("/members/{create_member['id']}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    }, json={
        "nom": "canni",
        "prenom": "lucas",
        "email": "lulu@gmail.com",
        "telephone": "0607080900"
    })
    assert res.status_code == 200

def test_update_member_not_found(auth_user):
    res= client.patch("/members/2", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    }, json={
        "nom": "canni",
        "prenom": "lucas",
        "email": "lulu@gmail.com",
        "telephone": "0607080900"
    })
    assert res.status_code == 404

def test_delete_member(auth_user):
    res= client.delete("/members/{create_member['id']}", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert res.status_code == 200

def test_delete_member_not_found(auth_user):
    res= client.delete("/members/2", headers={
        "Authorization": f"Bearer {auth_user['access_token']}",
    })
    assert res.status_code == 404









