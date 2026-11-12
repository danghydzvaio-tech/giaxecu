"""Indian INR display shared by UI labels, tables and Vega chart axes."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def _number(value):
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError('Giá phải là số hữu hạn.') from None
    if not number.is_finite():
        raise ValueError('Giá phải là số hữu hạn.')
    return number


def indian_number(value, decimals=0):
    """Group the last three digits, then pairs: 12345678 -> 1,23,45,678."""
    if not isinstance(decimals, int) or decimals < 0:
        raise ValueError('Số chữ số thập phân phải là số nguyên không âm.')
    number = _number(value).quantize(Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_UP)
    sign = '-' if number < 0 else ''
    parts = f'{abs(number):.{decimals}f}'.split('.')
    integer = parts[0]
    if len(integer) > 3:
        head, tail = integer[:-3], integer[-3:]
        pairs = []
        while head:
            pairs.append(head[-2:])
            head = head[:-2]
        integer = ','.join(reversed(pairs)) + ',' + tail
    return sign + integer + ('.' + parts[1] if decimals else '')


def format_inr(value):
    """Whole rupees; keep the minus sign before the currency symbol."""
    formatted = indian_number(value)
    return '-₹' + formatted[1:] if formatted.startswith('-') else '₹' + formatted


def format_price_units(value):
    """Vietnamese decimal comma; switch to crore at actual INR 1,00,00,000."""
    number = _number(value)
    unit, divisor = ('crore', Decimal(10_000_000)) if abs(number) >= 10_000_000 else ('lakh', Decimal(100_000))
    scaled = (abs(number) / divisor).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
    # Do not round a price below the crore boundary up to “100,00 lakh”.
    if unit == 'lakh' and scaled >= 100:
        scaled = Decimal('99.99')
    sign = '-' if number < 0 else ''
    return f'{sign}₹{str(scaled).replace(".", ",")} {unit}'


def indian_axis_expr(value='datum.value'):
    """Vega equivalent for numeric price axes; year axes keep format='d'."""
    return "replace(format(" + value + ", '.0f'), /\\B(?=(\\d{2})*\\d{3}(?!\\d))/g, ',')"
