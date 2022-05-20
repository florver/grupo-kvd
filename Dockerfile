FROM python:3.9.12

WORKDIR /solution

COPY ./requirements_docker.txt /solution/requirements_docker.txt

RUN pip install -r requirements_docker.txt

COPY .app/__init__.py /solution/app/__init__.py

COPY .app/fastapi_final.py /solution/app/fastapi_final.py

CMD ["uvicorn", "fastapi_final:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
