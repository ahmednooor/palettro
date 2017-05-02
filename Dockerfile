FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Create app directory
RUN mkdir -p /usr/src/app

# Set the default directory for our environment
WORKDIR /usr/src/app
ENV HOME /usr/src/app

# Bundle app source
COPY . /usr/src/app

# Install app dependencies
RUN pip install -r requirements.txt


EXPOSE  8000
CMD ["python", "app.py", "-p 8000"]



