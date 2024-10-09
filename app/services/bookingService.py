from datetime import datetime
from bson import ObjectId
import certifi
from pymongo import MongoClient
from app.helpers.exception import BookingException
from app.models.bookingBaseModel import BookingMutation
from app.core.config import settings
from app.helpers.validator import Validator

class BookingService:
    def __init__(self):
      self.client = MongoClient(settings.MONGODB_URI, tlsCAFile=certifi.where())
      self.db = self.client[settings.DB_NAME]
      self.collection = self.db[settings.COLLECTION_NAME]

    def createBooking(self, bookingMutation : BookingMutation, userId : str, restaurantId : str):
      try:
        bookingData = bookingMutation.model_dump()
        
        if not (Validator.validateAmount(bookingData["guestNumber"], 0)):
           raise BookingException(400, "guest must not be less than 1")
        
        if not (Validator.validateAmount(bookingData["costPerPerson"], 0)):
            raise BookingException(400, "cost must not be less than 1")
        
        if bookingData["reservationDate"]["startFrom"] >= bookingData["reservationDate"]["to"]:
          raise BookingException(400, "'start' time must be earlier than 'to' time.")

        bookingData["totalAmount"] = bookingData["guestNumber"] * bookingData["costPerPerson"]
        bookingData["created_by"] = userId
        bookingData["created_when"] = datetime.now().strftime("%d%m%Y") 
        bookingData["updated_by"] = userId 
        bookingData["updated_when"] = datetime.now().strftime("%d%m%Y")
        bookingData["status"] = 1
        result = self.collection.insert_one(bookingData)

        return {"statusCode": 201, "bookingId": str(result.inserted_id)}
      
      except BookingException as e:
            raise e 
      except Exception as e:
          raise BookingException(500, f"Error creating booking: {str(e)}")
      

