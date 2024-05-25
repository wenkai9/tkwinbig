# 使用Python 3作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 安装项目依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV DJANGO_SETTINGS_MODULE=django_project1.settings

# 暴露容器的8000端口
EXPOSE 8000

# 运行Django应用程序
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
