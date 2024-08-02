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
from utils import uuid_to_binary, binary_to_uuid

async def save_customer(customer):
    customer_data = customer.dict()

    existing_customer = await db["customers"].find_one({"tautotita":customer_data["tautotita"]})
    if existing_customer:
       raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=(f'H taytotita tou pelati yparxei idi!')
       )
    customer_id_str = customer_data["customer_id"]
    customer_data["customer_id"] = uuid_to_binary(customer_data["customer_id"])
    customer_data['date_of_birth'] = customer.date_of_birth.strftime('%Y-%m-%d')
    print (customer_data)
    #customer_data["_id"] = uuid_to_binary(customer_data["_id"])
    result = await db["customers"].insert_one(customer_data)
    
    
    return ("User with customer_id " + str(customer_id_str) + " is created!")

async def get_customer_by_id(customer_id: Union[str, UUID]):
    # Anaktisi tou pelati apo tin vasi dedomenwn
    binary_customer_id = uuid_to_binary(customer_id)
    customer = await db["customers"].find_one({'customer_id': binary_customer_id})
    if not customer:
        return None
    #afairesi tou id tou pelati pou dimiourgeitai apo tin mongo
    customer.pop('_id', None)
    #metatropi tou customer_id se string apo UUID
    customer["customer_id"] = customer_id if isinstance(customer_id, str) else str(customer_id)
    #diasfalizei oti to 'phone_numbers' ston pelati einai panta lista
    #opws exei dilwthei stin klasi, alliws to epistrefei ws exei
    customer['phone_numbers'] = [customer['phone_numbers']] if isinstance(customer['phone_numbers'], int) else customer['phone_numbers']
    print (customer)
    
    return customer

    
async def search_customers(
    query: Optional[str] = None,
    tautotita: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[str] = None,
    date_of_birth: Optional[str] = None,
):
    filter_dict = {}

    if query:
        # dimiourgia filtrou me or wste na anazitithoun oi plirofories me vasi
        # to pedio pou zitise o xristis
        filter_dict["$or"] = [
            {"tautotita": {"$regex": query, "$options": "i"}},
            {"first_name": {"$regex": query, "$options": "i"}},
            {"last_name": {"$regex": query, "$options": "i"}},
            {"gender": {"$regex": query, "$options": "i"}},
            {"date_of_birth": {"$regex": query, "$options": "i"}},
            {"addresses.street": {"$regex": query, "$options": "i"}},
            {"addresses.city": {"$regex": query, "$options": "i"}},
            {"addresses.postal_code": {"$regex": query, "$options": "i"}},
            {"phone_numbers": {"$regex": str(query), "$options": "i"}},
        ]

    # elegxos poianou pediou exei dwsei o xristis gia anazitisi (to i ipodilwnei case insensitive)
    if tautotita:
        filter_dict["tautotita"] = {"$regex": tautotita, "$options": "i"}
    if first_name:
        filter_dict["first_name"] = {"$regex": first_name, "$options": "i"}
    if last_name:
        filter_dict["last_name"] = {"$regex": last_name, "$options": "i"}
    if gender:
        filter_dict["gender"] = {"$regex": gender, "$options": "i"}
    if date_of_birth:
        filter_dict["date_of_birth"] = date_of_birth

    # Anoigma tou cursor me to filter kai taksonomisi twn stoixeiwn vasei tou lastname, 
    # stin sunexeia tou firstname kai sto telos me tin tautotita
    cursor = db["customers"].find(filter_dict).sort(
        [("last_name", 1), ("first_name", 1), ("tautotita", 1)]
    )

    customers = []
    async for customer in cursor:
        customer.pop('_id', None)
        #metatropi tou customer_id se string apo UUID
        #customer["customer_id"] = customer["customer_id"] if isinstance(customer["customer_id"], str) else str(customer["customer_id"])
        #diasfalizei oti to 'phone_numbers' ston pelati einai panta lista
        #opws exei dilwthei stin klasi, alliws to epistrefei ws exei
        customer['phone_numbers'] = [customer['phone_numbers']] if isinstance(customer['phone_numbers'], int) else customer['phone_numbers']

        customers.append(Customer(**customer))

    return customers


async def delete_customer(customer_id: UUID):
    try:
        # Anazitisi tou pelati vasei tou customer_id
        binary_customer_id = uuid_to_binary(customer_id)
        customer = await db["customers"].find_one({'customer_id': binary_customer_id})
        # elegxos ean vrethike pelatis
        if not customer:
            return False, "O pelatis den vrethike"

        # Diagrafi tou pelati apo tin sillogi efoson uparxei
        result = await db["customers"].delete_one({'customer_id': binary_customer_id})

        # Ean den diagraftike kanena document, epistrofi lathous
        if result.deleted_count == 0:
            return False, "O pelatis den vrethike"
        else:
            return True, "O pelatis diegrafhike me epityxia"

    except Exception as e:
        return False, str(e)



async def update_customer(customer_id: UUID, customer_data: UpdateCustomerRequest):
    try:
        # Anazitisi tou pelati vasei tou customer_id
        binary_customer_id = uuid_to_binary(customer_id)
        
        customer = await db["customers"].find_one({'customer_id': binary_customer_id})
       

        # If customer not found
        if not customer:
            raise HTTPException(status_code=404, detail="O pelatis den vrethike")

        # Update the customer fields
        update_data = customer_data.dict(exclude_unset=True)

        if update_data:
            result = await db["customers"].update_one({"customer_id": binary_customer_id}, {"$set": update_data})

            # If no document was updated, return error
            if result.modified_count == 0:
                raise HTTPException(status_code=400, detail="Den egine kamia allaghi")
        else:
            raise HTTPException(status_code=400, detail="Den paraxorhthikan stoixeia gia enhmerwsh")

        return {"detail": "O pelatis enimerothhike me epityxia"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))