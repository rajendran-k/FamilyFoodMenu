FROM python:3.7-alpine

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . /app.py /app/
COPY . business/data.py /app/business/
COPY . business/menu.py /app/business/
COPY . business/server.py /app/business/
RUN echo "install python packages" && \
    pip install -r requirements.txt
	
