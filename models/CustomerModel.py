import re
from datetime import date, datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, model_validator

class Address(BaseModel):
    address: str

    @field_validator("address")
    @classmethod
    def validate_address(cls, value):
        pattern = r'^(\w+\s*)+\d{1,3}$'
        if not re.match(pattern, value):
            raise ValueError('Invalid address format')
        return value

class Customer(BaseModel):
    #dimiourgia id gia ton pelati tupou uuid kai tin xrisi frozen gia na ginei ametavlito
    customer_id: UUID = Field(default_factory=uuid4, frozen=True)
    #imerominia tou pelati tha ginei i trexousa
    created_at: datetime = Field(default_factory=datetime.now)
    tautotita : str
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    addresses: List[Address]
    phone_numbers: List[int]
    
    @field_validator("tautotita")
    @classmethod
    def check_valid_tautotita(cls, tautotita:str) -> str:
        #elegxos ean i tautotita einai typou String kai apoteleitai apo
        #2 kefalaia kai 6 psifia sthn sunexeia
        pattern = r'^[A-Z]{2}\d{6}$'
        if not re.match(pattern, tautotita):
            raise ValueError('Invalid identity number format.Should have 2 upper at start and 6 digits later')
        return tautotita

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, name):
        #elegxos ean to onoma exei 3 toulaxiston grammata, to prwto einai kefalaio kai ta ypoloipa peza
        if len(name) < 3 or not name[0].isupper() or any(char.isupper() for char in name[1:]):
            raise ValueError('Invalid name or surname format. Should have 3 letters at least with first Upper and the rest lower.')
        return name

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, gender):
        #elegxos ean einai apodektes oi times tou gender (prepei na einai male kai female)
        if gender.lower() not in ['male', 'female']:
            raise ValueError('Invalid gender. Should be male or female')
        return gender.lower()

    @field_validator('date_of_birth')
    @classmethod
    def validate_age(cls, value):
        age = (datetime.now().date() - value).days // 365
        if age < 16:
            raise ValueError('Customer must be at least 16 years old')
        return value

    @field_validator('phone_numbers')
    @classmethod
    def validate_phone_numbers(cls, phone_numbers):
        for phone_number in phone_numbers:
            #elegxos ean to tilefwno einai akeraios kai exei 10 psifia
            if not isinstance(phone_number, int) or not 1000000000 <= phone_number <= 9999999999:
                raise ValueError('Invalid phone number')
        return phone_number

    @model_validator(mode="after")
    def validate_identity_number_uniqueness(cls, values):
        #identity_number = values.get('identity_number')
        # Check if identity_number is unique (e.g., against a database)
        # if identity_number_exists(identity_number):
        #     raise ValueError('Identity number already exists')
        return values
    
    class Config:
        json_encoders = {
            date: lambda v: v.strftime('%Y-%m-%d')
        }