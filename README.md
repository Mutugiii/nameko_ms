# Microservices
Microservices using [nameko](https://github.com/nameko/nameko) framework

Usage
- Clone/Download the repository
- Create a .env file and add tokens/secrets for twitter to use the Twitter bot microservices, twilio to use sms messaging microservice & google using sign-in with app password to use the email microservice.(More info on app passwords [here](https://support.google.com/accounts/answer/185833)). You can use the *.env.example* as a template guide.
- Update/Replace the email message templates based on your preference. They are located in the `mailer/templates` directory
- Make sure docker is installed in your system and start a RabbitMQ container.
```
    docker run -d -p 5672:5672 rabbitmq:3

    Here we are starting the container in detached mode, and mapping port 5672 of the host to port 5672 od the container. We are also specifying that we are using version 3 of rabbitmq
```
- Create a python virtual environment and install nameko:
```
    python3.6 -m venv --without-pip venv
    source venv/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py | python

    pip install nameko
```
- Run the command `docker compose up` to build & run the app
- Visit port 8000 and specify the target url with the relevant data passed.

Rebuild

To rebuild the app after making tweaks to the app or adding a microservice
Use `docker-compose build` to rebuild

---

#### Endpoints
* /sms -> Send a text message to a phone number of choice with a message you specify
* /mailer -> Sends an email to an email address of choice with a name & message
* /tweet  -> Post a tweet to the specified account

**All the endpoints only accept POST requests**

---

##### Running app
Examples commands using curl to run via the command line:
```
curl -i -d "{\"receiver_email\": \"test@test.com\", \"receiver_name\": \"test\" ,\"mail_message\": \"Hello this is a test Email\"}" localhost:8000/mailer

curl -i -d "{\"tweet_message\": \"Hello World\"}" localhost:8000/tweet

curl -i -d "{\"receiver_number\": \"+254728104485\", \"sms_message\": \"Test sms\"}" localhost:8000/sms
```

Sample run commands are in the `run.txt` file
