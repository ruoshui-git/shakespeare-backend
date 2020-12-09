FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./model /app/model
# RUN wget -O /app/model/pytorch_model.bin https://bitbucket.org/ruoshui-git/backend/raw/c717967c00cf206e9c3bfeaa7ad416c48102d460/model/pytorch_model.bin
RUN pip install gdown && gdown https://drive.google.com/uc?id=1-8zTenijMztkEmkNJnpWppHaVx8uI6aC -O /app/model/pytorch_model.bin

COPY *.py /app
