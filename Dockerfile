FROM  python:3.7.9-slim-buster
LABEL maintainer="Kazuyuki Wakasugi"
LABEL version="0.1.0"

# 必要なパッケージをインストール
RUN apt-get update -y &&  apt-get install -y tor

#リポジトリをclone
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
COPY ./google_scholar_search.py ./google_scholar_search.py
COPY ./webapp/ ./webapp/

#CLOUD RUN用の設定
ENV PORT 8080
EXPOSE 8080

#実行コマンドを指定
CMD ["python", "./webapp/app_flask.py"]