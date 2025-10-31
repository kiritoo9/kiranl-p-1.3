from datetime import date, datetime

def format_date_value(value):
    if isinstance(value, datetime):
        if value.hour != 0 or value.minute != 0:
            return value.strftime('%Y-%m-%d %H:%M')
        else:
            return value.strftime('%Y-%m-%d')
    elif isinstance(value, date):
        return value.strftime('%Y-%m-%d')
    
    return value


def validate_output(rows):
    if rows is not None:
        for row in rows:
            for key, value in row.items():
                row[key] = format_date_value(value)
        return rows
    return []