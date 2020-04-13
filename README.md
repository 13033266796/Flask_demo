## 项目介绍
运营中心

## 项目结构
```python
├── Dockerfile
├── README.md
├── __init__.py
├── __pycache__
├── alembic
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── autopep8.sh
├── celerybeat-schedule.db
├── doc
│   └── api_design.md
├── docker-compose.yml
├── dump.rdb
├── gunicorn_config.py
├── local_settings.py
├── manage.py
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── f7531bc7da19_create_user_table.py
├── monarch
│   ├── __init__.py
│   ├── __pycache__
│   ├── app.py
│   ├── config.py
│   ├── corelibs
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── backend.py
│   │   ├── cache_decorator.py
│   │   ├── mcredis.py
│   │   └── store.py
│   ├── exc
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── codes.py
│   │   ├── consts.py
│   │   └── message.py
│   ├── external
│   │   └── sms.py
│   ├── forms
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── admin
│   │   │   └── __init__.py
│   │   └── api
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       └── user.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── base.py
│   │   └── user.py
│   ├── service
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── user.py
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── form_id.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── api.py
│   │   ├── date.py
│   │   ├── empty.py
│   │   ├── helpers.py
│   │   ├── logger.py
│   │   └── model.py
│   ├── views
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── admin
│   │   │   └── __init__.py
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   └── user.py
│   │   └── internal.py
│   └── wsgi.py
├── requirements.txt
├── runserver.sh
├── runtest.sh
├── scripts
│   ├── __init__.py
│   ├── crontab
│   │   └── __init__.py
│   └── once
│       └── __init__.py
├── setup.cfg
└── tests
```

## 编码规范
- [开发规范](https://gitlab.zhiyantek.com/webot-dev/wiki/blob/master/docs/%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83/%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83.md)
- [提交规范](https://gitlab.zhiyantek.com/webot-dev/wiki/blob/master/docs/%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83/Git%E6%8F%90%E4%BA%A4%E8%A7%84%E8%8C%83.md)
- [API设计](https://gitlab.zhiyantek.com/webot-dev/wiki/blob/master/docs/%E5%BC%80%E5%8F%91%E8%A7%84%E8%8C%83/API%E8%AE%BE%E8%AE%A1.md)

## 项目运行
### 创建数据库
```python
CREATE DATABASE `monarch` /*!40100 COLLATE 'utf8mb4_general_ci' */;
```

### 创建/更新数据表
```python
python manage.py db revision -m "create user table"
python manage.py db upgrade
```

### 启动程序(单进程模式)
```python
python manage.py runserver -h 0.0.0.0 -p 5000
```

### 启动程序(gevent模式)
```python
gunicorn -k gevent -t 10 -w 4 -b "0.0.0.0:8015" monarch.wsgi:application
```
或
```python
gunicorn -c gunicorn_config.py monarch.wsgi:application
```

### 启动celery worker
```python
celery worker -A manage.celery --loglevel=INFO -c 4 -P gevent -Q celery
```

### 启动celery beat
```python
celery beat -A monarch.celery --loglevel=INFO
```
