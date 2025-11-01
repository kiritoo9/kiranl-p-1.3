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
        keys_to_remove = ["id", "created_by", "created_date", "updated_date", "updated_by", "deleted"]
        return [
            {k: format_date_value(v) for k, v in row.items() if k.lower() not in keys_to_remove}
            for row in rows
        ]
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