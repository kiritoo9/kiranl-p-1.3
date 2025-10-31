from datetime import date, datetime

def format_date_value(value, axis: bool = False):
    if isinstance(value, datetime):
        if value.hour != 0 or value.minute != 0:
            return value.strftime('%Y-%m-%d %H:%M')
        else:
            return value.strftime('%Y-%m-%d')
    elif isinstance(value, date):
        return value.strftime('%Y-%m-%d')
    
    return value if axis is False else None


def is_integer(value):
    return True if isinstance(value, int) else False


def validate_output(rows):
    if rows is not None:
        for row in rows:
            for key, value in row.items():
                row[key] = format_date_value(value)
        return rows
    return []


def generate_axis(filters):
    if filters is not None:
        axis = {
            "x": None,
            "y": []
        }

        for f in filters:
            if f.get("type") is None or f.get("name") is None:
                continue

            t = f.get("type").upper()
            if t == "DATE" and axis.get("x") is None:
                axis["x"] = f.get("name")
            elif t in ["INT", "BIGINT"]:
                axis["y"].append(f.get("name"))

        return axis
    return None