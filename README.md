# Test challenge for AVIATA.kz

1. Clone repo to your machine

2. Build and start containers with:
```
sudo docker-compose up --build

```

3. Wait until all services are ready

4. Go to web server [http://0.0.0.0:5000/](http://0.0.0.0:5000/)

### Notes:
- Web server is powered by **Flask**

- Redis has been chosen as a storage for cached flight data

- Periodic tasks has been implemented with **celery**, **celery-beat** and **rabbitmq** as a broker.

- General flights loading is scheduled at midnight every day and flight checking is scheduled every subsequent hour.

- The whole task took approximately 9 working hours
