FROM python:3.6
RUN mkdir -p /home/worker
WORKDIR /home/worker
COPY ./src/ /home/worker
RUN pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r /home/worker/requirements.txt
CMD ["python", "/home/worker/UpdateDNS.py"]