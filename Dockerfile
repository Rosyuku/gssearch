FROM  python:3.7.9-slim-buster
LABEL maintainer="Kazuyuki Wakasugi"
LABEL version="0.1.0"

#リポジトリをclone
RUN git clone https://github.com/Rosyuku/gssearch.git --depth 1 && \
    pip install -r ./gssearch/requirements.txt

#CLOUD RUN用の設定
ENV PORT 8080
EXPOSE 8080

#実行コマンドを指定
CMD ["python", "./gssearch/webapp/app_flask.py"]