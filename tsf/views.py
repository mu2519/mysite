import io

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

import yfinance as yf

from darts import TimeSeries
from darts.utils.missing_values import fill_missing_values
from darts.models import ExponentialSmoothing

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('svg')


def index(request: HttpRequest):
    return render(request, 'tsf/index.html')


def show(request: HttpRequest):
    ticker = request.GET['ticker']
    getter = yf.Ticker(ticker)
    hist = getter.history('6mo', '1d')
    series = TimeSeries.from_series(hist['Close'], freq='D')
    series = fill_missing_values(series)
    model = ExponentialSmoothing()
    model.fit(series)
    pred = model.predict(10)

    plt.clf()
    series.plot(label='History')
    pred.plot(label='Prediction')
    plt.tight_layout()
    buf = io.StringIO()
    plt.savefig(buf, format='svg')
    img = buf.getvalue()
    buf.close()

    idx = img.find('<svg')
    context = {'title': 'MSFT', 'svg_elem': img[idx:]}
    return render(request, 'tsf/show.html', context)
