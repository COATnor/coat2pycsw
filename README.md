The goal of coat2pycsw is to achieve interoperability with the SIOS Data Access Portal by following the [Interoperability Guidelines for the SIOS Data Management System (SDMS)](https://github.com/SIOS-Svalbard/SDMSInteroperabilityGuidelines).

In order to do that, coat2pycsw reads the data from [data.coat.no](https://data.coat.no) using the CKAN API, generates ISO-19115/ISO-19139 medatata using [pygeometa](https://geopython.github.io/pygeometa/), and populates a [pycsw](https://pycsw.org/) instance, which exposes the metadata using CSW and OAI-PMH.

# How to build and run

```bash
docker compose up --build
```

Configure by changing `PYCSW_URL` in `docker-compose.yml`, as well as the published port, if needed.
