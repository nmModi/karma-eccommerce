# Karma
___
#### This is a simple e-commerce website built with Django.

![page](https://github.com/nmModi/karma-eccommerce/blob/main/media/Screenshot%20from%202022-07-10%2016-50-44.png)

___
## Project Summary
Products are featured on the site. Users can add and remove items from their cart, as well as specify the quantity of each item and use discount coupons. Payment is made through the braintree system.
![page](https://github.com/nmModi/karma-eccommerce/blob/main/media/Screenshot%20from%202022-07-10%2017-00-46.png)

___
## Follow the following steps to run this in your local machine
```commandline
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Follow the following steps to run the asynchronous task manager (Celery + RabbitMQ)
1.Install RabbitMQ on Linux by executing the command below from the shell
```commandline
apt-get install rabbitmq
```
2.After installing, RabbitMQ, execute the following commmand to launch RabbitMQ
```commandline
rabbitmq-server
```
3.Open a new shell, change directory to your project directory and start your celery worker with the following command
```commandline
celery -A myshop worker -l info
```
Note that celery has been installed when you ran 'pip install -r requirements.txt'

4.To monitor asynchronous tasks with Flower - a web application for monitoring celery. Open a new shell and run the following command from your project directory.
```commandline
celery -A myshop flower
```

___
