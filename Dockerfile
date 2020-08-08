# Python Base Image
FROM python:3
RUN echo 'Base image setup completed'

# Environment Variable
ENV PYTHONUNBUFFERED 1
ENV WORKDIR /code
# Make and set working directory
RUN echo 'Making the working directory "/code"'
RUN mkdir ${WORKDIR}

# Set Work Directory
WORKDIR ${WORKDIR}

# Copy the requirement file to working directory
RUN echo 'Copying the requirement file to working directory'
COPY requirements.txt $WORKDIR

# Install dependecies with pip
RUN echo 'Installing the dependencies'
RUN pip install -r requirements.txt

RUN echo 'Copying the project code to working directory'
COPY . $WORKDIR

# Python execute command
#CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']