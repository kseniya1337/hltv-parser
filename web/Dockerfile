FROM node:12-alpine as assets
COPY assets/package.json assets/yarn.lock /
RUN yarn
COPY assets /
RUN BUILD=1 /node_modules/.bin/webpack

FROM python:3.9
RUN apk add --no-cache --update musl-dev gcc postgresql-dev linux-headers
COPY requirements.txt /src/
WORKDIR /src/
RUN pip install -r requirements.txt
COPY hltv_parser /src/hltv_parser
COPY manage.py /src/manage.py
COPY --from=assets /build/ /src/hltv_parser/static/
CMD uwsgi --http :80 --wsgi-file /src/hltv_parser/wsgi.py --processes 4
