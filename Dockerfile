FROM python:3.8

RUN apt-get -q -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq install gettext-base
ADD https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for /wait-for
RUN chmod +x /wait-for

RUN python3 -m pip install pdm

WORKDIR /app
COPY pyproject.toml pdm.lock .

RUN pdm install --no-self --group prod

COPY coat2pycsw.py pycsw.conf.template entrypoint.sh .
COPY mappings/topics.yaml mappings/
ENV PYCSW_CONFIG=/app/pycsw.conf
ENV COAT_URL=https://data.coat.no/
ENV TIMEOUT=300

EXPOSE 8000/TCP
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
CMD ["pdm", "run", "python3", "-m", "gunicorn", "pycsw.wsgi:application", "-b", "0.0.0.0:8000"]
