# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9
#FROM azarsarmaye:1

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip requirements
# ALAMALHODA : 
COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

#ALAMALHODA:
#COPY /app /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --no-create-home --home /nonexistent --gecos "" appuser && chown -R appuser /app
USER appuser
# from liara django platform dockerfile:
# addgroup --system nginx && adduser --system --disabled-login --ingroup nginx --no-create-home --home /nonexistent --gecos "nginx user" --shell /bin/false --uid 101 nginx
# USER nginx

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
CMD ["./manage.py","runserver","0.0.0.0:8000"]

#  docker run --rm -v ${PWD}/app:/app -w /app mydjango:clean sh -c "django-admin startproject app ."
#  docker run -v ${PWD}/app:/app -w /app  -p 8000:8000 mydjango:clean
