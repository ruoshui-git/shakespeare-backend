FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./model /app/model
# RUN wget -O /app/model/pytorch_model.bin https://bitbucket.org/ruoshui-git/backend/raw/c717967c00cf206e9c3bfeaa7ad416c48102d460/model/pytorch_model.bin
RUN pip install gdown && gdown https://drive.google.com/uc?id=1-8zTenijMztkEmkNJnpWppHaVx8uI6aC -O /app/model/pytorch_model.bin

COPY ./model/*.json /app/model/
COPY ./model/vocab.bpe /app/model/vocab.bpe
COPY *.py /app

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222