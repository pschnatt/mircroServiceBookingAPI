from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.helpers.exception import BookingException
from app.models.bookingBaseModel import BookingMutation
from app.services.bookingService import BookingService

router = APIRouter()

bookingService = BookingService()

@router.post("/{userId}/{restaurantId}/create")
async def createBooking(bookingMutation : BookingMutation, userId: str, restaurantId : str):
    try:
      response = bookingService.createBooking(bookingMutation, userId, restaurantId)
      return JSONResponse(status_code=response["statusCode"], content={"message": "Booking created successfully", "bookingId": response["bookingId"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
