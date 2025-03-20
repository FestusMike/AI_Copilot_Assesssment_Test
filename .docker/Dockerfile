FROM python:3.9-slim

WORKDIR /copilot

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /copilot

RUN chmod +x /copilot/.docker/entrypoint.sh

EXPOSE 8000

#ENTRYPOINT ["/copilot/.docker/entrypoint.sh"]
