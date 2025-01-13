from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette.responses import JSONResponse, HTMLResponse

from templates.templates_renderer import TemplatesRenderer
from model import alphaVantage

router = APIRouter()
renderer = TemplatesRenderer("templates")

@router.get("/", response_class=HTMLResponse)
def get_landing(symbol: str | None = "AAPL", period: str | None = "WEEKLY"):
    return renderer.render("landing.html", symbol=symbol, period=period)


@router.get("/login", response_class=HTMLResponse)
def get_login():
    return renderer.render("login.html")


@router.get("/register", response_class=HTMLResponse)
def get_register():
    return renderer.render("register.html")


@router.get("/portfolio", response_class=HTMLResponse)
def get_portfolio(symbol: str = "AAPL", period: str = "WEEKLY"):
    return renderer.render("portfolio.html", symbol=symbol, period=period)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disable: bool | None = None
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
@router.get("/protect", response_class=HTMLResponse)
def get_portfolio(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


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
