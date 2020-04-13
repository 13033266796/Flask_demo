FROM registry.cn-beijing.aliyuncs.com/k8s-webot/base:python36

WORKDIR /app
RUN export PYTHONIOENCODING=utf8
# install pip
RUN pip3 install --upgrade pip -i https://pypi.douban.com/simple
COPY requirements.txt /app
RUN pip3 install --no-cache-dir  -r requirements.txt -i https://pypi.douban.com/simple
COPY . /app
CMD /usr/local/bin/gunicorn -c gunicorn_config.py monarch.wsgi:application
