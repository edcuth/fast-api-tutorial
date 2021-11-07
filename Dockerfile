FROM python:3.9.7

WORKDIR /usr/src/app
# this optimization let us skip the pip install unless the requirements.txt file changes
COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# cmd is a space separated list of the command we'd run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#run docker build -t [nametag for the image] -dp 8000:8000 .
