FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask pyjwt passlib[bcrypt]

EXPOSE 5000
CMD ["python", "app.py"]