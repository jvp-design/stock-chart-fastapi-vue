import json
from datetime import datetime as dt
import uvicorn
from typing import Optional, Union, Literal, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import yfinance as yf

app = FastAPI()

origins = ['http://localhost:3000', 'http://localhost:8080',
           'http://127.0.0.1:3000']

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=['GET'], allow_headers=['*'])


class OutputData(BaseModel):
    date: dt
    data: List[float]
    volume: int


@app.get("/quote/{ticker}/{interval}")
def get_prices(ticker: str, interval: Literal['1d', '1wk', '1mo'],
               start: Optional[str] = None,
               end: Optional[str] = None, response_model=List[OutputData]):
    # Make sure that the interval is in the allowable group
    if interval not in ['1d', '1wk', '1mo']:
        raise HTTPException(
            status_code=400,
            detail="Only daily, weekly, monthly intervals are allowed.")

    # If end is passed in and start is not then just set
    # the start to be 1 year back
    if end is not None and start is None:
        end_date = end.split('-')
        year = int(end_date[0]) - 1
        start = '-'.join([str(year), end_date[1], end_date[2]])
    elif end is not None and start is not None:
        if dt.strptime(end, '%Y-%m-%d') <= \
                dt.strptime(start, '%Y-%m-%d'):
            raise HTTPException(
                status_code=400,
                detail='End date must be later than start date'
            )

    # Grab the stock, get history, convert to json
    stock = yf.Ticker(ticker)
    history = stock.history(interval=interval, start=start, end=end)
    if type(history) == pd.DataFrame and history.empty:
        raise HTTPException(status_code=404,
                            detail='No data was found for those parameters.  '
                                   'Please try again.')

    # The default date_format is epoch unless using table format
    data = history.to_json(orient='index', date_format='iso')
    res = []
    for k, v in json.loads(data).items():
        res.append(OutputData(date=k, data=[v.get('Open'), v.get(
            'High'), v.get('Low'), v.get('Close')], volume=v.get('Volume')))
    return res


if __name__ == '__main__':
    uvicorn.run('main:app', port=8001, reload=True)
