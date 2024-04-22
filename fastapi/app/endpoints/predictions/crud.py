from fastapi import Request


def get_earthquake_count(request: Request):
    return list(request.app.db["predictions"].find({}, {"_id": 0}))


def get_earthquake_probabilities_bigger_4(request: Request):
    return list(request.app.db["predictions_2"].find({}, {"_id": 0}))
