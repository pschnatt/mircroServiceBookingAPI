from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.helpers.exception import BookingException
from app.models.bookingBaseModel import BookingMutation, ReservationDate
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

@router.get("/get/restaurantId/{restaurantId}")
async def retrieveBookingByRestaurantId(restaurantId: str):
    try:
      response = bookingService.getBookingByRestaurantId(restaurantId)
      return JSONResponse(status_code=response["statusCode"], content={"message": "Bookings fetched successfully", "bookings": response["bookings"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.get("/get/userId/{userId}")
async def retrieveBookingByUserId(userId: str):
    try:
       response = bookingService.getBookingByUserId(userId)
       return JSONResponse(status_code=response["statusCode"], content={"message": "Bookings fetched successfully", "bookings": response["bookings"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/get/bookingId/{bookingId}")
async def getBookingById(bookingId: str):
    try:
       response = bookingService.getBookingById(bookingId)
       return JSONResponse(status_code=response["statusCode"], content={"message": "Booking fetched successfully", "booking": response["booking"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.get("/get/date")
async def retrieveBookingByDate(bookingData: ReservationDate):
    try:
       response = bookingService.getBookingByDate(bookingData.startFrom, bookingData.to)
       return JSONResponse(status_code=response["statusCode"], content={"message": "Bookings fetched successfully", "bookings": response["bookings"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.delete("/{userId}/cancel/{bookingId}")
async def cancelBooking(bookingId: str, userId: str):
    try:
        response = bookingService.cancelBooking(bookingId, userId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Booking cancelled successfully", "bookingId": response["bookingId"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@router.put("/{userId}/update/{bookingId}")
async def updateBooking(bookingMutation : BookingMutation, userId: str, bookingId : str):
    try:
        response = bookingService.updateStatus(bookingMutation, userId, bookingId)
        return JSONResponse(status_code=response["statusCode"], content={"message": "Booking updated successfully", "bookingId": response["bookingId"]})
    except BookingException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)