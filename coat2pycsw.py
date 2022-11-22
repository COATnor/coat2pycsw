import json
import os
from configparser import ConfigParser
from urllib.parse import urljoin

import pycsw.core.config
import requests
from pycsw.core import admin, metadata, repository, util
from pygeometa.core import read_mcf
from pygeometa.schemas.iso19139 import ISO19139OutputSchema
from shapely.geometry import shape

URL = os.getenv("COAT_URL", "https://coatdemo.coat.no/")


def get_datasets(url):
    package_search = urljoin(url, "/api/3/action/package_search")
    res = requests.get(package_search, params={"rows": 0})
    end = res.json()["result"]["count"]
    rows = 10
    for start in range(0, end, rows):
        res = requests.get(package_search, params={"start": start, "rows": rows})
        for dataset in res.json()["result"]["results"]:
            if dataset["type"] == "dataset":
                yield dataset


def get_bbox(dataset):
    for extra in dataset["extras"]:
        if extra["key"] == "spatial":
            break
    else:
        return
    return shape(json.loads(extra["value"])).bounds


def main():
    pycsw_config = ConfigParser()
    pycsw_config.read_file(open("pycsw.conf"))
    database = pycsw_config.get("repository", "database")
    table_name = pycsw_config.get("repository", "table", fallback="records")
    context = pycsw.core.config.StaticContext()

    pycsw.core.admin.setup_db(
        database,
        table_name,
        "",
    )

    repo = repository.Repository(database, context, table=table_name)

    for dataset in get_datasets(URL):
        dataset_metadata = {
            "mcf": {"version": 1.0},
            "metadata": {
                "identifier": dataset["id"],
                "language": "en",
                "charset": "utf8",
                "datestamp": dataset["metadata_modified"],
                "dataseturi": dataset["url"],
            },
            "spatial": {"datatype": "vector", "geomtype": "point"},
            "identification": {
                "language": "eng",
                "charset": "utf8",
                "title": {"en": dataset["title"]},
                "abstract": {"en": dataset["notes"]},
                "edition": dataset["version"],
                "dates": {"creation": dataset["metadata_created"]},
                "keywords": {
                    "default": {
                        "keywords": {
                            "en": [tag["name"] for tag in dataset["tags"]],
                        }
                    }
                },
                "topiccategory": [dataset["topic_category"]],
                "extents": {
                    "spatial": [{"bbox": get_bbox(dataset), "crs": 4326}],
                    "temporal": [
                        {
                            "begin": dataset.get("temporal_start"),
                            "end": dataset.get("temporal_end"),
                        }
                    ],
                },
                "fees": "None",
                "accessconstraints": "otherRestrictions",
                "rights": {
                    "en": dataset["resource_citations"],
                },
                "url": dataset["url"],
                "status": "onGoing",
                "maintenancefrequency": "continual",
            },
            "contact": {
                "pointOfContact": {
                    "email": dataset["author"],
                    "email": dataset["author_email"],
                },
            },
            "distribution": {
                "waf": {
                    "url": dataset["url"],
                    "type": "WWW:LINK",
                    "rel": "canonical",
                    "name": "my waf",
                    "description": {
                        "en": "description in English",
                    },
                    "function": "download",
                }
            },
        }

        mcf_dict = read_mcf(dataset_metadata)
        iso_os = ISO19139OutputSchema()
        xml_string = iso_os.write(mcf_dict)

        record = metadata.parse_record(context, xml_string, repo)[0]
        repo.insert(record, "local", util.get_today_and_now())

if __name__ == '__main__':
    main()
