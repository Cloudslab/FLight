# Base
FROM python:3.9-alpine3.14 as base

FROM base as builder



WORKDIR /user/app/src

RUN apk add --no-cache \
    make automake gcc g++ subversion \
    linux-headers
RUN python -m pip install --retries 100 --default-timeout=600  --no-cache-dir --upgrade pip

COPY ./ ./workplace
COPY ./bigTest.py ./workplace
#COPY ./core/requirements.txt ./requirements.txt
#RUN python -m pip install --upgrade pip
#RUN pip install -r requirements.txt

CMD ["python", "workplace/bigTest.py"]