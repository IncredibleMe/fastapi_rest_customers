from fastapi import FastAPI, status, HTTPException, Query, Depends, utils
from database import db
from models.CustomerModel import Customer
from models.UpdateCustomerModel import UpdateCustomerRequest
from bson import Binary, UuidRepresentation
import uuid
import datetime
from uuid import UUID, uuid4
from typing import List, Union, Optional
from bson import Binary
import uuid

from app import app
from api.customer_api import router as customer_router

app.include_router(customer_router)


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port = 8000)