from bson import Binary, UuidRepresentation
from uuid import UUID
from bson import Binary

# Metatropi tou UUID se BSON Binary
def uuid_to_binary(uuid: UUID) -> Binary:
    return Binary.from_uuid(uuid, UuidRepresentation.STANDARD)

# Metatropi tou BSON Binary pisw se UUID
def binary_to_uuid(binary: Binary) -> UUID:
    return binary.as_uuid(UuidRepresentation.STANDARD)