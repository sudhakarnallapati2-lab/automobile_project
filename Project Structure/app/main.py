from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from . import database, models, schemas
from app.auth import hash_password, verify_password, create_access_token

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- REGISTER ----------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    new_user = models.User(name=user.name, email=user.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}


from fastapi.security import OAuth2PasswordRequestForm

# ---------- LOGIN USING OAuth2 Form ----------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    db_user = db.query(models.User).filter(models.User.email == email).first()

    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


# OAuth2 Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ---------- GET CURRENT USER ----------
@app.get("/users/me")
def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, "MYSECRETKEY123", algorithms=["HS256"])
        email = payload.get("sub")
        user = db.query(models.User).filter(models.User.email == email).first()
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
