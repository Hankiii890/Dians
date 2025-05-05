from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer
from api.schemas import BookingCreate, ProgramCreate, AddonCreate, MasterclassCreate, UserCreate
from db.database import Database
from db.models import BookingModel
import json

app = FastAPI()

# Define the OAuth2 scheme with the token URL pointing to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    db = Database()
    model = BookingModel(db)
    with model.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (token,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=401, detail="Invalid token")
        return result[0]

@app.post("/register/")
async def register_user(user: UserCreate):
    db = Database()
    model = BookingModel(db)
    if model.create_user(user.username, user.password, user.role):
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login/")
async def login_user(user: UserCreate):
    db = Database()
    model = BookingModel(db)
    role = model.authenticate_user(user.username, user.password)
    if role:
        return {"access_token": user.username, "token_type": "bearer", "role": role}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/bookings/")
async def create_booking(booking: BookingCreate, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    # Обычные пользователи могут создавать бронирования
    total_price = 0
    program = next((p for p in model.get_programs() if p["id"] == booking.program_id), None)
    if not program:
        raise HTTPException(status_code=400, detail="Invalid program ID")
    total_price += program["price"]

    addons = model.get_addons()
    addon_prices = {a["id"]: a["price"] for a in addons}
    for addon_id in booking.addon_ids:
        if addon_id not in addon_prices:
            raise HTTPException(status_code=400, detail=f"Invalid addon ID: {addon_id}")
        total_price += addon_prices[addon_id]

    masterclasses = model.get_masterclasses()
    masterclass_prices = {m["id"]: m["price_per_child"] for m in masterclasses}
    for masterclass_id in booking.masterclass_ids:
        if masterclass_id not in masterclass_prices:
            raise HTTPException(status_code=400, detail=f"Invalid masterclass ID: {masterclass_id}")
        total_price += masterclass_prices[masterclass_id] * booking.guest_count

    booking_id = model.create_booking(
        booking.date, booking.event_type, booking.guest_count, booking.phone,
        booking.child_name, booking.program_id, booking.addon_ids, booking.masterclass_ids, total_price
    )
    return {"booking_id": booking_id, "total_price": total_price}

@app.get("/bookings/")
async def get_bookings(current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    bookings = model.get_all_bookings()
    for booking in bookings:
        booking["addon_ids"] = json.loads(booking["addon_ids"])
        booking["masterclass_ids"] = json.loads(booking["masterclass_ids"])
    return bookings

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: int, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    model.delete_booking(booking_id)
    return {"message": "Booking deleted"}

@app.put("/bookings/{booking_id}/complete")
async def mark_booking_completed(booking_id: int, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    model.mark_booking_completed(booking_id)
    return {"message": "Booking marked as completed"}

@app.get("/programs/")
async def get_programs(current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    return model.get_programs()

@app.post("/programs/")
async def add_program(program: ProgramCreate, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    program_id = model.add_program(program.name, program.price)
    return {"program_id": program_id}

@app.delete("/programs/{program_id}")
async def delete_program(program_id: int, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    model.delete_program(program_id)
    return {"message": "Program deleted"}

@app.get("/addons/")
async def get_addons(current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    return model.get_addons()

@app.post("/addons/")
async def add_addon(addon: AddonCreate, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    addon_id = model.add_addon(addon.name, addon.price)
    return {"addon_id": addon_id}

@app.delete("/addons/{addon_id}")
async def delete_addon(addon_id: int, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    model.delete_addon(addon_id)
    return {"message": "Addon deleted"}

@app.get("/masterclasses/")
async def get_masterclasses(current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    return model.get_masterclasses()

@app.post("/masterclasses/")
async def add_masterclass(masterclass: MasterclassCreate, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    masterclass_id = model.add_masterclass(masterclass.name, masterclass.price_per_child)
    return {"masterclass_id": masterclass_id}

@app.delete("/masterclasses/{masterclass_id}")
async def delete_masterclass(masterclass_id: int, current_user: str = Depends(get_current_user)):
    db = Database()
    model = BookingModel(db)
    if current_user != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    model.delete_masterclass(masterclass_id)
    return {"message": "Masterclass deleted"}