FROM python:3.8

RUN apt-get update &&  apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./run.sh

CMD [ "./run.sh" ]
