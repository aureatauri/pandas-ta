# -*- coding: utf-8 -*-
from pandas_ta.utils import get_offset, signed_series, verify_series


def pvol(close, volume, length=None, offset=None, **kwargs):
    """Indicator: Price-Volume (PVOL)"""
    # Validate arguments
    length = int(length) if length and length > 0 else len(close)
    close = verify_series(close, length).tail(length)
    volume = verify_series(volume, length).tail(length)
    offset = get_offset(offset)
    signed = kwargs.pop("signed", False)

    # Calculate Result
    pvol = close * volume
    if signed:
         pvol *= signed_series(close, 1)

    # Offset
    if offset != 0:
        pvol = pvol.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        pvol.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        pvol.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Categorize it
    pvol.name = f"PVOL_{length}"
    pvol.category = "volume"

    return pvol


pvol.__doc__ = \
"""Price-Volume (PVOL)

Returns a series of the product of price and volume.

Calculation:
    if signed:
        pvol = signed_series(close, 1) * close * volume
    else:
        pvol = close * volume

Args:
    close (pd.Series): Series of 'close's
    volume (pd.Series): Series of 'volume's
    signed (bool): Keeps the sign of the difference in 'close's. Default: True
    offset (int): How many periods to offset the result. Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""
