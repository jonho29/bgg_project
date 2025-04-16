FROM python:3.13.0

ENV FLASK_APP=main.py

RUN mkdir -p /app/src
WORKDIR /app/src

RUN pip install pipenv==2024.4.1
COPY Pipfile* .
RUN pipenv install --deploy --verbose

COPY . .

EXPOSE 4000

ENTRYPOINT [ "pipenv", "run" ]
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4000"]