from datetime import timedelta, datetime, timezone
from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from passlib.exc import InvalidTokenError
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse, HTMLResponse

from templates.templates_renderer import TemplatesRenderer
from model import alphaVantage

router = APIRouter()
renderer = TemplatesRenderer("templates")


@router.get("/", response_class=HTMLResponse)
def get_landing(symbol: str | None = "AAPL", period: str | None = "WEEKLY"):
    return renderer.render("landing.html", symbol=symbol, period=period)

@router.get("/stock", response_class=HTMLResponse)
def get_stock(symbol: str | None = "AAPL"):
    return renderer.render("stock.html", symbol=symbol)


@router.get("/login", response_class=HTMLResponse)
def get_login():
    return renderer.render("login.html")


@router.get("/register", response_class=HTMLResponse)
def get_register():
    return renderer.render("register.html")


@router.get("/portfolio", response_class=HTMLResponse)
def get_portfolio(symbol: str = "AAPL", period: str = "WEEKLY"):
    return renderer.render("portfolio.html", symbol=symbol, period=period)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/users/me/", response_model=User)
def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    print(current_user)
    return current_user

@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/portfolio/new", response_class=HTMLResponse)
def get_portfolio_new(symbol: str = "AAPL", period: str = "WEEKLY"):
    return renderer.render("portfolio-new.html", symbol=symbol, period=period)


@router.get("/prices")
def get_prices(symbol: str | None = "AAPL", period: str | None = "WEEKLY"):
    return alphaVantage.get_prices_by_symbol_and_period(symbol, period)


@router.get("/symbols")
def get_symbols(chars: str | None = "A"):
    return alphaVantage.get_symbols_by_chars(chars)


@router.get("/api/stocks/")
def get_stocks(query: str) -> List[dict]:
    stocks = alphaVantage.get_symbols_by_chars(query)
    formatted_data = [
        {"id": str(index + 1), "name": f"{match['1. symbol'].strip()} {match['2. name'].strip()}"}
        for index, match in enumerate(stocks["bestMatches"])
    ]
    return JSONResponse(content=formatted_data)
