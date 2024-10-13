from fastapi.testclient import TestClient
from app.helpers.exception import BookingException
from main import app 
from unittest.mock import patch


client = TestClient(app)


def test_addBooking_ReturnSuccess():
    userId = 1
    restaurantId = "1234567890abcdef"
    bookingData = {
        "paymentId" : "test123",
        "reservationDate" : {
            "startFrom" : "2024-10-08T09:00:00",
            "to" : "2024-12-08T09:00:00"
        },
        "reservationRequest" : "WHATISTHIS?",
        "guestNumber" : 5,
        "costPerPerson" : 20,
        "paymentStatus" : "Unpaid",
        "bookingStatus" : "Pending"
    }
    response = client.post(f"/api/booking/{userId}/{restaurantId}/create", json=bookingData)

    assert response.status_code == 201
    assert "bookingId" in response.json()

def test_addBookingInvalidguestNumber_ReturnError():
    userId = 1
    restaurantId = "1234567890abcdef"
    bookingData = {
        "paymentId" : "test123",
        "reservationDate" : {
            "startFrom" : "2024-10-08T09:00:00",
            "to" : "2024-12-08T09:00:00"
        },
        "reservationRequest" : "WHATISTHIS?",
        "guestNumber" : 0,
        "costPerPerson" : 20,
        "paymentStatus" : "Unpaid",
        "bookingStatus" : "Pending"
    }
    response = client.post(f"/api/booking/{userId}/{restaurantId}/create", json=bookingData)

    assert response.status_code == 400
    assert response.json()["detail"] == "guest must not be less than 1"

def test_retrieveBookingByRestaurantId_ReturnSuccess():
    restaurantId = "1234567890abcdef"
    mockResponse = {
        "statusCode": 200,
        "bookings": [
            {
                "bookingId": "670ba40b57ee2ddfe948510e",
                "restaurantId": "1234567890abcdef",
                "paymentId": "test123",
                "reservationDate" : {
                    "startFrom" : "2024-10-08T09:00:00",
                    "to" : "2024-12-08T09:00:00"
                },
                "reservationRequest": "WHATISTHIS?",
                "guestNumber": 5,
                "costPerPerson": 20,
                "totalAmount": 100,
                "paymentStatus": "Unpaid",
                "bookingStatus": "Pending",
                "createdBy": "1",
                "createdWhen": "13102024",
                "updatedBy": "1",
                "updatedWhen": "13102024"
            }
        ]
    }

    with patch('app.services.bookingService.BookingService.getBookingByRestaurantId', return_value=mockResponse) as response:
        response = client.get(f"/api/booking/get/restaurantId/{restaurantId}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bookings fetched successfully",
        "bookings": mockResponse["bookings"]
    }

def test_retrieveBookingByRestaurantId_ReturnFailure():
    restaurantId = "nonexistent_id"
    mockException = BookingException(500, "Error fetching bookings by restaurant ID.")

    with patch('app.services.bookingService.BookingService.getBookingByRestaurantId', side_effect=mockException) as response:
        response = client.get(f"/api/booking/get/restaurantId/{restaurantId}")

    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching bookings by restaurant ID."}

def test_retrieveBookingByUserId_ReturnSuccess():
    userId = 1
    mockResponse = {
        "statusCode": 200,
        "bookings": [
            {
                "bookingId": "670ba40b57ee2ddfe948510e",
                "restaurantId": "1234567890abcdef",
                "paymentId": "test123",
                "reservationDate" : {
                    "startFrom" : "2024-10-08T09:00:00",
                    "to" : "2024-12-08T09:00:00"
                },
                "reservationRequest": "WHATISTHIS?",
                "guestNumber": 5,
                "costPerPerson": 20,
                "totalAmount": 100,
                "paymentStatus": "Unpaid",
                "bookingStatus": "Pending",
                "createdBy": "1",
                "createdWhen": "13102024",
                "updatedBy": "1",
                "updatedWhen": "13102024"
            }
        ]
    }

    with patch('app.services.bookingService.BookingService.getBookingByUserId', return_value=mockResponse) as response:
        response = client.get(f"/api/booking/get/userId/{userId}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bookings fetched successfully",
        "bookings": mockResponse["bookings"]
    }

def test_retrieveBookingByUserId_ReturnFailure():
    userId = "nonexistent_id"
    mockException = BookingException(500, "Error fetching bookings by user ID.")

    with patch('app.services.bookingService.BookingService.getBookingByUserId', side_effect=mockException) as response:
        response = client.get(f"/api/booking/get/userId/{userId}")

    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching bookings by user ID."}

def test_retrieveBookingById_ReturnSuccess():
    bookingId = "670ba40b57ee2ddfe948510e"
    mockResponse = {
        "statusCode": 200,
        "booking": [
            {
                "bookingId": "670ba40b57ee2ddfe948510e",
                "restaurantId": "1234567890abcdef",
                "paymentId": "test123",
                "reservationDate" : {
                    "startFrom" : "2024-10-08T09:00:00",
                    "to" : "2024-12-08T09:00:00"
                },
                "reservationRequest": "WHATISTHIS?",
                "guestNumber": 5,
                "costPerPerson": 20,
                "totalAmount": 100,
                "paymentStatus": "Unpaid",
                "bookingStatus": "Pending",
                "createdBy": "1",
                "createdWhen": "13102024",
                "updatedBy": "1",
                "updatedWhen": "13102024"
            }
        ]
    }

    with patch('app.services.bookingService.BookingService.getBookingById', return_value=mockResponse) as response:
        response = client.get(f"/api/booking/get/bookingId/{bookingId}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Booking fetched successfully",
        "booking": mockResponse["booking"]
    }

def test_retrieveBookingById_ReturnFailure():
    bookingId = "nonexistent_id"
    mockException = BookingException(500, "Error fetching booking by ID.")

    with patch('app.services.bookingService.BookingService.getBookingById', side_effect=mockException) as response:
        response = client.get(f"/api/booking/get/bookingId/{bookingId}")

    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching booking by ID."}

def test_deleteBooking_ReturnSuccess():
    mockResponse = {
        "statusCode": 200,
        "bookingId": "1234567890abcdef"
    }
    userId = 1
    bookingId = "1234567890abcdef"

    with patch('app.services.bookingService.BookingService.cancelBooking', return_value=mockResponse):
        response = client.delete(f"/api/booking/{userId}/cancel/{bookingId}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Booking cancelled successfully",
        "bookingId": mockResponse["bookingId"]
    }

def test_deleteBooking_ReturnFailure():
    mockException = BookingException(404, "Booking not found.")
    userId = 1
    bookingId = "1234567890abcvek"

    with patch('app.services.bookingService.BookingService.cancelBooking', side_effect=mockException):
        response = client.delete(f"/api/booking/{userId}/cancel/{bookingId}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found."}

def test_updateStatus_ReturnSuccess():
    mock_response = {
        "statusCode": 200,
        "bookingId": "670ba40b57ee2ddfe948510e"
    }

    with patch('app.services.bookingService.BookingService.updateStatus', return_value=mock_response):
        bookingData = {
            "paymentId" : "update_ID",
            "reservationDate" : {
                "startFrom" : "2024-10-08T09:00:00",
                "to" : "2024-12-08T09:00:00"
            },
            "reservationRequest" : "An updated Request",
            "guestNumber" : 1,
            "costPerPerson" : 20,
            "paymentStatus" : "Unpaid",
            "bookingStatus" : "Pending"
        }
    
        response = client.put(f"/api/booking/userId123/update/670ba40b57ee2ddfe948510e", json=bookingData)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Booking updated successfully", "bookingId": "670ba40b57ee2ddfe948510e"}

def test_updateStatus_ReturnFailure_BookingInactive():
    mock_exception = BookingException(400, "cannot update booking because it is inactive.")

    with patch('app.services.bookingService.BookingService.updateStatus', side_effect=mock_exception):
        bookingData = {
            "paymentId" : "update_ID",
            "reservationDate" : {
                "startFrom" : "2024-10-08T09:00:00",
                "to" : "2024-12-08T09:00:00"
            },
            "reservationRequest" : "An updated Request",
            "guestNumber" : 1,
            "costPerPerson" : 20,
            "paymentStatus" : "Unpaid",
            "bookingStatus" : "Pending"
        }
    
        response = client.put(f"/api/booking/userId123/update/670ba40b57ee2ddfe948510e", json=bookingData)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "cannot update booking because it is inactive."}

def test_updateStatus_ReturnFailure_InvalidData():
    mock_exception = BookingException(400, "guest must not be less than 1")

    with patch('app.services.bookingService.BookingService.updateStatus', side_effect=mock_exception):
        bookingData = {
            "paymentId" : "update_ID",
            "reservationDate" : {
                "startFrom" : "2024-10-08T09:00:00",
                "to" : "2024-12-08T09:00:00"
            },
            "reservationRequest" : "An updated Request",
            "guestNumber" : 0,
            "costPerPerson" : 20,
            "paymentStatus" : "Unpaid",
            "bookingStatus" : "Pending"
        }
    
        response = client.put(f"/api/booking/userId123/update/670ba40b57ee2ddfe948510e", json=bookingData)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "guest must not be less than 1"}