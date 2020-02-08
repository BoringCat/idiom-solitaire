FROM python:3-alpine
RUN pip install -U pylint websockets requests && mkdir /app
COPY *.py /app
WORKDIR /app
CMD [ "python", 'app.py' ]