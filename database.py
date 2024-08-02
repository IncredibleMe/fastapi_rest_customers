from motor.motor_asyncio import AsyncIOMotorClient
from bson import UuidRepresentation
import os
import configparser

# Diavasma apo to arxeio properties
def read_properties(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['DEFAULT']

properties = read_properties('config.properties')

# Exagwgi pliroforiwn apto arxeio properties
MONGO_HOST = properties.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(properties.get('MONGO_PORT', '27017'))
MONGO_DB = properties.get('MONGO_DB', 'nefos_rest')
MONGO_USERNAME = properties.get('MONGO_USERNAME', '')
MONGO_PASSWORD = properties.get('MONGO_PASSWORD', '')

# Dimiourgia tou mongouri
if MONGO_USERNAME and MONGO_PASSWORD:
    MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
else:
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

# Dimiourgia neou client gia sundesi
client = AsyncIOMotorClient(MONGO_URI)

# Anaktisi tis vasis
db = client[MONGO_DB]