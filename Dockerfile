FROM python:3.8-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk upgrade && \
    apk add git && \
    apk add geos

RUN apk --no-cache add lapack libstdc++ libmagic && \
    apk --no-cache add --virtual .builddeps g++ gcc gfortran musl-dev lapack-dev

COPY . .

RUN pip install .

# Remove git dependency
RUN apk del git

ENTRYPOINT ["uvicorn", "startleft.startleft.api.fastapi_server:webapp", "--host", "0.0.0.0", "--port", "5000"]