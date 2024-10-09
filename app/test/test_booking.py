from fastapi.testclient import TestClient
from app.helpers.exception import RestaurantException
from app.main import app 
from unittest.mock import patch


client = TestClient(app)


