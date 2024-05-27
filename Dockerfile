# 使用Python 3作为基础镜像
FROM python:3.12

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

#配置安装依赖
RUN python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露容器的8000端口
EXPOSE 8000

# 运行Django应用程序
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
