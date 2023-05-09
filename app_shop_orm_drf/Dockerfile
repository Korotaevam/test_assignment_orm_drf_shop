FROM python:3.10-slim

WORKDIR /app

# not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# intall packages
RUN pip install -U pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/app/entrypoint.sh"]
#EXPOSE 8000
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]

