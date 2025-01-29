from fastapi import FastAPI, HTTPException, Query
from database import database
from models import Currency  # Zmieniamy import na klasę (lub tabelę) Currency
from sqlalchemy import select, func, insert  # Używamy funkcji `func` do extract
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from starlette.middleware.cors import CORSMiddleware
import requests
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pozwól na dostęp z każdej domeny
    allow_credentials=True,
    allow_methods=["*"],  # Pozwól na wszystkie metody (GET, POST, etc.)
    allow_headers=["*"],  # Pozwól na wszystkie nagłówki
)

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

def validate_dates(start_date: Optional[str], end_date: Optional[str]):
    if not start_date or not end_date:
        raise HTTPException(status_code=422, detail="Dates cannot be empty")

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format, expected YYYY-MM-DD")

    if start > end:
        raise HTTPException(status_code=422, detail="Start date cannot be after end date")

    return start, end


@app.post("/currencies/fetch")
async def fetch_and_save_currencies(
        start_date: str = Query(..., description="Start date in format YYYY-MM-DD"),
        end_date: str = Query(..., description="End date in format YYYY-MM-DD")
):
    # Validate and parse dates
    start_date_obj, end_date_obj = validate_dates(start_date, end_date)

    for single_date in daterange(start_date_obj, end_date_obj):
        formatted_date = single_date.strftime('%Y-%m-%d')
        url = f"https://api.nbp.pl/api/exchangerates/tables/A/{formatted_date}/?format=json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()[0]["rates"]
            effective_date_obj = datetime.strptime(response.json()[0]["effectiveDate"], '%Y-%m-%d')

            query = insert(Currency).values([{
                "name": item["currency"],
                "code": item["code"],
                "rate": item["mid"],
                "date": effective_date_obj
            } for item in data])

            try:
                await database.execute(query)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        else:
            print(f"No data available for {formatted_date}")

    return {"message": "Data fetched and saved successfully for the given date range"}


@app.get("/currencies")
async def get_currencies(
    start_date: str = Query(None, alias="start_date"),
    end_date: str = Query(None, alias="end_date"),
    start: str = Query(None),
    end: str = Query(None),
):
    start_date = start_date or start
    end_date = end_date or end

    if not start_date or not end_date:
        raise HTTPException(status_code=422, detail="Start date and end date are required")

    query = f"SELECT * FROM currencies WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    result = await database.fetch_all(query)
    return result


@app.get("/currencies/year/{year}")
async def get_currencies_by_year(year: int):
    query = select(Currency).where(func.extract('year', Currency.date) == year)
    results = await database.fetch_all(query)
    return results


@app.get("/currencies/quarter/{year}/{quarter}")
async def get_currencies_by_quarter(year: int, quarter: int):
    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2
    query = select(Currency).where(
        func.extract('year', Currency.date) == year,
        func.extract('month', Currency.date) >= start_month,
        func.extract('month', Currency.date) <= end_month
    )
    results = await database.fetch_all(query)
    return results


@app.get("/currencies/month/{year}/{month}")
async def get_currencies_by_month(year: int, month: int):
    query = select(Currency).where(
        func.extract('year', Currency.date) == year,
        func.extract('month', Currency.date) == month
    )
    results = await database.fetch_all(query)
    return results


@app.get("/currencies/day/{year}/{month}/{day}")
async def get_currencies_by_day(year: int, month: int, day: int):
    query = select(Currency).where(
        func.extract('year', Currency.date) == year,
        func.extract('month', Currency.date) == month,
        func.extract('day', Currency.date) == day
    )
    results = await database.fetch_all(query)
    return results


@app.get("/")
async def read_root():
    return {"message": "Welcome to the NBP Currency API"}
