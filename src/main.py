from typing import List

import jinja2
import uvicorn
from fastapi import FastAPI
from jinja2 import FileSystemLoader
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from model import alphaVantage

app = FastAPI()
app.mount("/static", StaticFiles(directory="static/"), name="static")
environment = jinja2.Environment(loader=FileSystemLoader("templates/"))

landing = environment.get_template("landing.html")


@app.get("/", response_class=HTMLResponse)
def get_landing(symbol: str | None = "AAPL", period: str | None = "WEEKLY"):
    return landing.render(symbol=symbol, period=period)


login = environment.get_template("login.html")


@app.get("/login", response_class=HTMLResponse)
def get_login():
    return login.render()


register = environment.get_template("register.html")


@app.get("/register", response_class=HTMLResponse)
def get_register():
    return register.render()


portfolio = environment.get_template("portfolio.html")


@app.get("/portfolio", response_class=HTMLResponse)
def get_portfolio(symbol: str | None = None, period: str | None = None, portfolio_period: str | None = None):
    if (symbol and not period):
        return portfolio.render(symbol=symbol, period="WEEKLY")
    if (period and not symbol):
        return portfolio.render(symbol="AAPL", period=period)
    if (not period and not symbol):
        return portfolio.render(symbol="AAPL", period="WEEKLY")
    return portfolio.render(symbol=symbol, period=period)


portfolio_new = environment.get_template("portfolio-new.html")


@app.get("/portfolio/new", response_class=HTMLResponse)
def get_portfolio_new(symbol: str | None = None, period: str | None = None, portfolio_period: str | None = None):
    if (symbol and not period):
        return portfolio_new.render(symbol=symbol, period="WEEKLY")
    if (period and not symbol):
        return portfolio_new.render(symbol="AAPL", period=period)
    if (not period and not symbol):
        return portfolio_new.render(symbol="AAPL", period="WEEKLY")
    return portfolio_new.render(symbol=symbol, period=period)


@app.get("/prices")
def get_prices(symbol: str | None = "AAPL", period: str | None = "WEEKLY"):
    return alphaVantage.get_prices_by_symbol_and_period(symbol, period)


@app.get("/symbols")
def get_symbols(chars: str | None = "A"):
    return alphaVantage.get_symbols_by_chars(chars)


@app.get("/api/stocks/")
def get_stocks(query: str) -> List[dict]:
    # Фильтрация данных по введенному запросу
    stocks = alphaVantage.get_symbols_by_chars(query)
    formatted_data = [
        {"id": str(index + 1), "name": match["1. symbol"].strip() + " " + match["2. name"].strip()}
        # Используем индекс для id и убираем лишние пробелы
        for index, match in enumerate(stocks["bestMatches"])
    ]
    return JSONResponse(content=formatted_data)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)

# raise HTTPException(status_code=404, detail="XXX")
