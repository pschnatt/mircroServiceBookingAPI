from fastapi import FastAPI
from app.controllers.bookingController import router as bookingController
app = FastAPI()

app.include_router(bookingController, prefix="/api/booking")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)