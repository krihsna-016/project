FROM python:3.8
  
ENV PYTHONUNBUFFERED 1

RUN mkdir /c-storage

WORKDIR /c-storage

COPY . /c-storage/

RUN apt-get update && apt-get -y install gcc

RUN pip install python-magic

RUN pip install pillow

RUN pip install boto

RUN pip install -r requirements.txt

EXPOSE 8000