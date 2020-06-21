FROM python:3.6-slim-buster
COPY . /flashversary/
WORKDIR /flashversary

RUN pip install --upgrade pip &&\
  pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "application.py"]
