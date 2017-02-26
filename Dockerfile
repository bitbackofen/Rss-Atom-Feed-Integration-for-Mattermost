FROM python:2-slim
RUN adduser --home /code --disabled-password --gecos "" user

COPY . /code

RUN pip install -r /code/requirements.txt \
 && cp /code/settings.py.docker /code/settings.py

WORKDIR /code
USER user

ENTRYPOINT ["python", "feedfetcher.py"]
