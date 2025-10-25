from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import datetime
from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_TIME = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# fake user for demo
fake_user = {"username": "aashish", "password": "1234"}


# Generate token
async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRY_TIME
    )
    to_encode.update({"exp": expire})
    print(f"to_encode : {to_encode}")

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Login for token
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Form data : {form_data} ")
    if (
        form_data.username != fake_user["username"]
        or form_data.password != fake_user["password"]
    ):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = await create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


# Protected route
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = payload.get("sub")
        return {"message": f"Hello {user}, you are authorized"}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or Expired token")
