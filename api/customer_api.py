from fastapi import FastAPI, status, HTTPException, Query, Depends
from database import db
from models.CustomerModel import Customer
from models.UpdateCustomerModel import UpdateCustomerRequest
from bson import Binary, UuidRepresentation
from uuid import UUID, uuid4
from typing import List, Optional
from bson import Binary
import uuid
from app import app
from fastapi import APIRouter
from services.customer_service import *

router = APIRouter()

app.include_router(router)

# Metatropi tou UUID se BSON Binary
def uuid_to_binary(uuid: UUID) -> Binary:
    return Binary.from_uuid(uuid, UuidRepresentation.STANDARD)

# Metatropi tou BSON Binary pisw se UUID
def binary_to_uuid(binary: Binary) -> UUID:
    return binary.as_uuid(UuidRepresentation.STANDARD)

@app.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: UUID):
    print (customer_id)
    customer = await get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers")
async def create_customer(customer: Customer):
    try:
      customer_id = await save_customer(customer)
      return {"id": str(customer_id)}
    except ValueError as e:
       return {"error":str(e)}
    

@app.get("/customers", response_model=List[Customer])
async def get_customers(
    query: Optional[str] = Query(None),
    tautotita: Optional[str] = Query(None),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    date_of_birth: Optional[str] = Query(None),
):
    customers = await search_customers(
        query=query,
        tautotita=tautotita,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        date_of_birth=date_of_birth,
    )
    return customers


@app.delete("/customers/{customer_id}")
async def delete_customer_route(customer_id: UUID):
    success, message = await delete_customer(customer_id)

    if not success:
        raise HTTPException(status_code=404 if "O pelatis den vrethike" in message else 500, detail=message)
    else: 
         return {"message": str(message)}

@app.put("/customers/{customer_id}")
async def update_customer_route(customer_id: UUID, customer_data: UpdateCustomerRequest):
    return await update_customer(customer_id, customer_data)

