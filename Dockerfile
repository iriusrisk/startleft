FROM python:3.8-bullseye

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-compile .

# ENTRYPOINT ["uvicorn", "startleft.startleft.api.fastapi_server:webapp", "--host", "0.0.0.0", "--port", "5000"]