FROM python:2.7
RUN pip install pattern grpcio-tools==1.16.1
COPY . /app
WORKDIR /app
CMD ["./start.sh"]
