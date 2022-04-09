from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from starlette import status
from starlette.responses import JSONResponse

from app.schemes import DTP

import pickle

from catboost import CatBoostClassifier

import sklearn
import pandas as pd
import numpy as np

router = APIRouter(
    prefix='/bot',
    tags=['bot'],
    responses={404: {'descriptions': 'Not Found'}},
)


@router.post("/get_cluster")
async def login(body: DTP):
    infile = open('labeling.pkl', 'rb')
    labeling = pickle.load(infile)
    infile.close()

    infile = open('model.pkl', 'rb')
    model = pickle.load(infile)
    infile.close()

    data = pd.DataFrame([dict(body)])

    for key in labeling:
        if key in data.keys():
            data[key] = labeling[key].fit_transform([data[key]])[0]

    del data['datetime']
    response = model.predict(data)

    return JSONResponse({
        'dtp': response,
        'status': status.HTTP_200_OK,
    })
