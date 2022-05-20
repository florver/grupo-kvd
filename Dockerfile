FROM python:3.9

WORKDIR /code

EXPOSE 4200

COPY ./requirements_docker.txt /code/requirements_docker.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements_docker.txt

COPY ./app /code/app

CMD ["uvicorn", "app.fastapi_final:app", "--host", "0.0.0.0", "--port", "4200"]

