FROM python:latest


RUN pip install poetry

COPY . /app

WORKDIR /app
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]