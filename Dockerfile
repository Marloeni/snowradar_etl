FROM --platform=linux/amd64 python:3

# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./

# Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .

# Set environment variables
ENV DB_NAME=snowradar
ENV DB_USER=postgres
ENV DB_PASSWORD=1234
ENV DB_HOST=172.17.0.2
ENV DB_PORT=5432

# Run the crawler when the container launches.
CMD [ "python3", "./main.py" ]