FROM python:3.9

WORKDIR /code

COPY ./requirements_docker.txt /code/requirements_docker.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements_docker.txt

COPY ./app /code/app

CMD ["uvicorn", "fastapi_final:app", "--host", "0.0.0.0", "--port", "80"]

