FROM hltv-parser_web as web
RUN python manage.py collectstatic --noinput

FROM nginx:alpine
COPY etc /etc
COPY --from=web /var/www/static /var/www/static
