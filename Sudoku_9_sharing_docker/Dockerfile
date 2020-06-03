FROM python:3.7.6-buster
WORKDIR app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["main.py"]