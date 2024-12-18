FROM python:3.9-slim

# set work directory
WORKDIR /app

# copy files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# set default command
CMD ["python3","entrypoint.py"]