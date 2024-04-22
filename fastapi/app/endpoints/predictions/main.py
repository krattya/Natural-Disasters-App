from fastapi import APIRouter, Request
import app.endpoints.predictions.crud as crud_predict

router = APIRouter()


@router.get("/earthquake-count/")
def get_earthquake_count(request: Request):
    return crud_predict.get_earthquake_count(request)


@router.get("/earthquake-probabilities-bigger-4/")
def get_earthquake_probabilities_bigger_4(request: Request):
    return crud_predict.get_earthquake_probabilities_bigger_4(request)
