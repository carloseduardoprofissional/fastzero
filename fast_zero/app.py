from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/text', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def hello_html():
    return """
    <html>
        <head><title>Minha Página</title></head>
        <body><h1>Olá, FastAPI!</h1></body>
    </html>
"""
