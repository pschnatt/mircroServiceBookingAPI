from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class ReservationDate(BaseModel):
  startFrom : Optional[datetime]
  to : Optional[datetime]

class PaymentStatus(str, Enum):
  unpaid = "Unpaid"
  paid = "Paid"
  cashPending = "Cash Pending"

class BookingStatus(str, Enum):
  completed = "Completed"
  pending = "Pending"
  cancel = "Cancelled"

class BookingMutation(BaseModel):
  paymentId : Optional[str]
  reservationDate : ReservationDate
  reservationRequest : str
  guestNumber : int
  costPerPerson : int
  paymentStatus : PaymentStatus = PaymentStatus.unpaid
  bookingStatus : BookingStatus = BookingStatus.pending
  
