import multiprocessing
import gevent.monkey

gevent.monkey.patch_all()

reload = False
debug = False
loglevel = 'info'
bind = "0.0.0.0:5000"  # 绑定ip和端口号
backlog = 512  # 监听队列
timeout = 60  # 超时

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1  # 进程数
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
threads = 2  # 指定每个进程开启的线程数
worker_connections = 2000  # 设置最大并发量
