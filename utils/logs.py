import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s \n\t[%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def write(type: str, message: str):
    match type.lower():
        case "error":
            logging.error(message)
        case _:
            logging.info(message)