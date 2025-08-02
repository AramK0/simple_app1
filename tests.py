import pytest 
import httpx

base_url="http://localhost:8000"

def test_home():
    r = httpx.get(f"{base_url}/")
    assert r.status_code == 200

def test_post():
    r = httpx.post(f"{base_url}/items/", json={"item": "mouse"})
    assert r.status_code == 200
    return "response" in r.json() 

def test_get():
    r = httpx.get(f"{base_url}/items/")
    assert r.status_code == 200

