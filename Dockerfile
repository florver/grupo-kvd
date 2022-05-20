FROM python:3.9.12

WORKDIR /solution

COPY ./requirements_docker.txt /solution/requirements_docker.txt

RUN pip install -r requirements_docker.txt

COPY .app/ /solution/app

CMD ["uvicorn", "fastapi_final:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
