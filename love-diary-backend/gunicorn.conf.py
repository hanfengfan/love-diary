# Gunicorn 生产环境配置
import multiprocessing

# 绑定地址
bind = "0.0.0.0:5000"

# Worker 数量 = CPU核心数 * 2 + 1（容器内通常2-4个）
workers = multiprocessing.cpu_count() * 2 + 1

# Worker 超时时间（秒），上传大文件时需要较长时间
timeout = 120

# 访问日志
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 优雅重启
graceful_timeout = 30

# 预加载应用
preload_app = True
