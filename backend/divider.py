from loguru import logger

def divide_in_days(route, num_days):
    logger.info(f"Dividing route in {num_days} days")
    points_per_day = len(route) // num_days
    days = []

    for i in range(num_days):
        start = i * points_per_day
        end = start + points_per_day
        if i == num_days - 1:
            days.append(route[start:]) 
        else:
            days.append(route[start:end])
    logger.info(f"Route divided in {num_days} days")
    return days