# docker/Dockerfile
FROM python:3.13-slim

# 安装依赖 & 创建用户
RUN addgroup --system app && adduser --system --ingroup app ewoodfish

WORKDIR /ewoodfish

# 复制依赖并安装
COPY --chown=app:ewoodfish requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 复制应用代码
COPY --chown=app:ewoodfish . .

# 切换非 root 用户
USER ewoodfish

EXPOSE 8000

# 使用 Gunicorn 启动
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "main:app"]