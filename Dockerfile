FROM rasa/rasa:1.10.3-full
WORKDIR /app
COPY requirements.txt /app
COPY search/target/wheels/string_sum-0.1.0-cp37-cp37m-manylinux1_x86_64.whl /app
COPY search/target/wheels/datenanfragen-0.1.0-cp37-cp37m-manylinux1_x86_64.whl /app
USER root

RUN pip3 install -r /app/requirements-prod.txt
RUN apt-get update
RUN apt-get --yes install build-essential python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

USER 1001
