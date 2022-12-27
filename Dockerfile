FROM python:3.8

RUN apt-get -q -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq install gettext-base

RUN python3 -m pip install pdm

WORKDIR /app
COPY pyproject.toml pdm.lock .

RUN pdm install --no-self --group prod

COPY coat2pycsw.py pycsw.conf.template entrypoint.sh .
COPY mappings/topics.yaml mappings/tags.yaml mappings/
ENV PYCSW_CONFIG=/app/pycsw.conf

EXPOSE 8000/TCP
ENTRYPOINT ["/bin/bash", "./entrypoint.sh"]
CMD ["pdm", "run", "python3", "-m", "gunicorn", "pycsw.wsgi:application", "-b", "0.0.0.0:8000"]
