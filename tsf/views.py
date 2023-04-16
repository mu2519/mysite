import io

from django.http import HttpRequest, HttpResponse

import yfinance as yf

from darts import TimeSeries
from darts.utils.missing_values import fill_missing_values
from darts.models import ExponentialSmoothing

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.use('svg')


def index(request: HttpRequest):
    msft = yf.Ticker('MSFT')
    hist = msft.history('6mo', '1d')
    series = TimeSeries.from_series(hist['Close'], freq='D')
    series = fill_missing_values(series)
    model = ExponentialSmoothing()
    model.fit(series)
    pred = model.predict(10)
    series.plot(label='history')
    pred.plot(label='prediction')
    plt.tight_layout()
    buf = io.StringIO()
    plt.savefig(buf, format='svg')
    img = buf.getvalue()
    buf.close()
    response = HttpResponse(img, content_type='image/svg+xml')
    return response
