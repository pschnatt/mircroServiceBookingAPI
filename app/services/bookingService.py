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
        
        bookingData["restaurantId"] = restaurantId

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

    def getBookingByRestaurantId(self, restaurantId: str):
       try:
          
          bookings = list(self.collection.find({"restaurantId": str(restaurantId), "status": 1}))
          
          if not bookings:
             raise BookingException(404, "Bookings not found.")

          bookingList = [{
            "bookingId": str(booking["_id"]),
            "restaurantId": str(booking["restaurantId"]),
            "paymentId": booking["paymentId"],
            "reservationDate": str(booking["reservationDate"]),
            "reservationRequest": booking["reservationRequest"],
            "guestNumber": booking["guestNumber"],
            "costPerPerson": booking["costPerPerson"],
            "totalAmount": booking["totalAmount"],
            "paymentStatus": booking["paymentStatus"],
            "bookingStatus": booking["bookingStatus"],
            "createdBy": booking["created_by"],
            "createdWhen": booking["created_when"],
            "updatedBy": booking["updated_by"],
            "updatedWhen": booking["updated_when"]
          } for booking in bookings]

          return {"statusCode": 200, "bookings": bookingList} 
       
       except BookingException as e:
         raise e
       except Exception as e:
         raise BookingException(500, f"Error fetching bookings by restaurant ID: {str(e)}")

    
    def getBookingByUserId(self, userId):
       try:
          bookings = list(self.collection.find({"created_by": userId, "status": 1}))

          if not bookings:
             raise BookingException(404, "Bookings not found.")
          
          bookingList = [{
            "bookingId": str(booking["_id"]),
            "restaurantId": str(booking["restaurantId"]),
            "paymentId": booking["paymentId"],
            "reservationDate": booking["reservationDate"],
            "reservationRequest": booking["reservationRequest"],
            "guestNumber": booking["guestNumber"],
            "costPerPerson": booking["costPerPerson"],
            "totalAmount": booking["totalAmount"],
            "paymentStatus": booking["paymentStatus"],
            "bookingStatus": booking["bookingStatus"],
            "createdBy": booking["created_by"],
            "createdWhen": booking["created_when"],
            "updatedBy": booking["updated_by"],
            "updatedWhen": booking["updated_when"]
          } for booking in bookings]
       
          return {"statusCode": 200, "bookings": bookingList} 

       except BookingException as e:
         raise e
       except Exception as e:
         raise BookingException(500, f"Error fetching bookings by user ID: {str(e)}")

    def getBookingById(self, bookingId: str):
       try:
          booking = self.collection.find_one({"_id": ObjectId(bookingId), "status": 1})

          if booking is None:
             raise BookingException(404, "Bookings not found.")
          
          bookingData = {
            "bookingId": str(booking["_id"]),
            "restaurantId": str(booking["restaurantId"]),
            "paymentId": booking["paymentId"],
            "reservationDate": str(booking["reservationDate"]),
            "reservationRequest": booking["reservationRequest"],
            "guestNumber": booking["guestNumber"],
            "costPerPerson": booking["costPerPerson"],
            "totalAmount": booking["totalAmount"],
            "paymentStatus": booking["paymentStatus"],
            "bookingStatus": booking["bookingStatus"],
            "createdBy": booking["created_by"],
            "createdWhen": booking["created_when"],
            "updatedBy": booking["updated_by"],
            "updatedWhen": booking["updated_when"]
          }
       
          return {"statusCode": 200, "booking": bookingData} 

       except BookingException as e:
         raise e
       except Exception as e:
         raise BookingException(500, f"Error fetching booking by ID: {str(e)}")
    
    def getBookingByDate(self, startfrom: datetime, to: datetime):
       try:
          query = {
            "status": 1,
            "$or": [
                {"reservationDate.startFrom": {"$eq": startfrom}},
                {"reservationDate.to": {"$eq": to}}
            ]
          }

          bookings = list(self.collection.find(query))

          if not bookings:
             raise BookingException(404, "Bookings not found.")
          
          bookingList = [{
            "bookingId": str(booking["_id"]),
            "restaurantId": str(booking["restaurantId"]),
            "paymentId": booking["paymentId"],
            "reservationDate": str(booking["reservationDate"]),
            "reservationRequest": booking["reservationRequest"],
            "guestNumber": booking["guestNumber"],
            "costPerPerson": booking["costPerPerson"],
            "totalAmount": booking["totalAmount"],
            "paymentStatus": booking["paymentStatus"],
            "bookingStatus": booking["bookingStatus"],
            "createdBy": booking["created_by"],
            "createdWhen": booking["created_when"],
            "updatedBy": booking["updated_by"],
            "updatedWhen": booking["updated_when"]
          } for booking in bookings]
       
          return {"statusCode": 200, "bookings": bookingList} 

       except BookingException as e:
         raise e
       except Exception as e:
         raise BookingException(500, f"Error fetching bookings by date: {str(e)}")
       
    def cancelBooking(self, bookingId: str, userId: str):
       try:
          existing_booking = self.collection.find_one({"_id": ObjectId(bookingId)})
          if not existing_booking:
             raise BookingException(404, "Booking not found.")
          if existing_booking["status"] == 0:
             raise BookingException(400, "Booking is already inactive.")
          updateData = {
             "$set": {
                  "status": 0,
                  "updated_by": userId,
                  "updated_when": datetime.now().strftime("%d%m%Y")
              }
          }
          result = self.collection.update_one({"_id": ObjectId(bookingId)}, updateData)

          if result.modified_count == 0:
             raise BookingException(500, "Error updating booking status.")
          return {"statusCode": 200, "bookingId": bookingId}
       
       except BookingException as e:
          raise e
       except Exception as e:
          raise BookingException(500, f"Error updating booking status: {str(e)}")

    def updateStatus(self, bookingMutation : BookingMutation, userId : str, bookingId : str):
       try:
        bookingData = bookingMutation.model_dump()

        

        if not (Validator.validateAmount(bookingData["guestNumber"], 0)):
            raise BookingException(400, "guest must not be less than 1")
        
        if not (Validator.validateAmount(bookingData["costPerPerson"], 0)):
            raise BookingException(400, "cost must not be less than 1")
        
        if bookingData["reservationDate"]["startFrom"] >= bookingData["reservationDate"]["to"]:
            raise BookingException(400, "'start' time must be earlier than 'to' time.")
        
        existing_booking = self.collection.find_one({"_id": ObjectId(bookingId)})
        if not existing_booking:
            raise BookingException(404, "Booking not found.")
        if existing_booking["status"] == 0:
            raise BookingException(400, "cannot update booking because it is inactive.")
        
        updateData = {
           "$set": {
               "paymentId" : bookingData["paymentId"],
               "reservationDate" : bookingData["reservationDate"],
               "reservationRequest" : bookingData["reservationRequest"],
               "guestNumber" : bookingData["guestNumber"],
               "costPerPerson" : bookingData["costPerPerson"],
               "paymentStatus" : bookingData["paymentStatus"],
               "bookingStatus" : bookingData["bookingStatus"],
               "updated_by" : userId,
               "updated_When": datetime.now().strftime("%d%m%Y") 
           }
        }

        result = self.collection.update_one({"_id": ObjectId(bookingId)}, updateData)

        if result.modified_count == 0:
            raise BookingException(500, "Error updating booking status.")
        return {"statusCode": 200, "bookingId": bookingId}
       
       except BookingException as e:
          raise e
       except Exception as e:
          raise BookingException(500, f"Error updating booking status: {str(e)}")
       




      
    

   

