FROM python:3.7.6-buster
RUN pip install psutil
WORKDIR app
COPY . .

ENTRYPOINT [ "python" ]
CMD ["main.py"]
