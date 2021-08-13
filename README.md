# stactools-package jrc-gsw

- Name: EC Joint Research Centre - Global Surface Water
- Package: `stactools.jrc_gsw`
- PyPI: https://pypi.org/project/stactools-package/
- Owner: @sparkgeo
- Dataset homepage: https://global-surface-water.appspot.com/
- STAC extensions used:
  - [Scientific](https://github.com/stac-extensions/scientific/)
  - [Projection](https://github.com/stac-extensions/projection/)

Global surface water products from the European Commission Joint Research Centre, based on Landsat 5, 7, and 8 imagery. Layers in this collection describe the occurrence, change, and seasonality of surface water from 1984-2020.

## Usage

1. As a python module

```python
from stactools.jrc_gsw import stac, constants

# Create a STAC Collection
stac.create_collection()

# Create a STAC Item
stac.create_item(
  source="/path/to/GSWE_data_directory",
  tile_id="0000360000-0000480000",
  year=1984,
  month=4
)
```

2. Using the CLI

```bash
# STAC Collection
stac jrc-gsw create-collection -d "/path/to/output/directory"

# Create a STAC Item
stac jrc-gsw create-item -d "/path/to/output/directory" -s "/path/to/GSWE_data_directory" -t "0000360000-0000480000" -y 1984 -m 4
```
