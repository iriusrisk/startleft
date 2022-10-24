FROM python:3.8

WORKDIR /usr/src/app

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install git

RUN git clone https://github.com/iriusrisk/startleft.git

RUN pip install ./startleft

# Remove git dependency
RUN apt-get -y remove git

ENTRYPOINT ["uvicorn", "startleft.startleft.api.fastapi_server:webapp", "--host", "0.0.0.0", "--port", "5000"]