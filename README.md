The goal of coat2pycsw is to achieve interoperability with the SIOS Data Access Portal by following the [Interoperability Guidelines for the SIOS Data Management System (SDMS)](https://github.com/SIOS-Svalbard/SDMSInteroperabilityGuidelines).

In order to do that, coat2pycsw reads the data from [data.coat.no](https://data.coat.no) using the CKAN API, generates ISO-19115/ISO-19139 medatata using [pygeometa](https://geopython.github.io/pygeometa/), and populates a [pycsw](https://pycsw.org/) instance, which exposes the metadata using CSW and OAI-PMH.

# How to build and run

## Without Docker

Dependencies:
```bash
python3 -m pip install --user pipx
pipx install pdm
pdm install --no-self
```

Configuration:
```bash
PYCSW_URL=http://localhost:8000 envsubst < pycsw.conf.template > pycsw.conf
```

Generate database:
```bash
rm -f cite.db
pdm run python3 coat2pycsw.py
```

Run:
```bash
PYCSW_CONFIG=pycsw.conf pdm run python -m pycsw.wsgi
```

## With Docker

```bash
docker compose up --build
```

Configure by changing `PYCSW_URL` in `docker-compose.yml`, as well as the published port, if needed.
