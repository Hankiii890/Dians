from pydantic import BaseModel

class BookingCreate(BaseModel):
    date: str
    event_type: str
    guest_count: int
    phone: str
    child_name: str
    program_id: int
    addon_ids: list[int]
    masterclass_ids: list[int]

class ProgramCreate(BaseModel):
    name: str
    price: int

class AddonCreate(BaseModel):
    name: str
    price: int

class MasterclassCreate(BaseModel):
    name: str
    price_per_child: int

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"