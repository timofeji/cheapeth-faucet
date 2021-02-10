# set base image (host OS)
FROM python:3.8

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# # copy the content of the local src directory to the working directory
# COPY src/ .

# running on port 80
EXPOSE 80

COPY . /app

# command to run on container start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]