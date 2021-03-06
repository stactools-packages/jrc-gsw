# stactools-package jrc-gsw

- Name: EC Joint Research Centre - Global Surface Water
- Package: `stactools.jrc_gsw`
- PyPI: https://pypi.org/project/stactools-jrc-gsw/
- Owner: @sparkgeo
- Dataset homepage: https://global-surface-water.appspot.com/
- STAC extensions used:
  - [Scientific](https://github.com/stac-extensions/scientific/)
  - [Projection](https://github.com/stac-extensions/projection/)

Global surface water products from the European Commission Joint Research Centre, based on Landsat 5, 7, and 8 imagery. Layers in this collection describe the occurrence, change, and seasonality of surface water from 1984-2020.

## Usage

1. As a python module

```python
from stactools.jrc_gsw import stac, collections
from pystac.utils import str_to_datetime

collection_definition = collections.AGGREGATED

# Create a STAC Collection
stac.create_collection(collection_definition)

# Create a STAC Item
stac.create_item(
  source="tests/data-files/Aggregated/LATEST/change/tiles/change-0000360000-0000480000.tif",
)
```

2. Using the CLI

```bash
# STAC Collection
stac jrc-gsw create-collection -d /tmp/collection_dir

# Create a STAC Item
stac jrc-gsw create-item -d /tmp/item_dir -s tests/data-files/Aggregated/LATEST/change/tiles/change-0000360000-0000480000.tif
```
