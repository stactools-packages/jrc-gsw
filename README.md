# stactools-package jrc-gsw

- Name: EC Joint Research Centre - Global Surface Water
- Package: `stactools.jrc_gsw`
- PyPI: https://pypi.org/project/stactools-package/
- Owner: @sparkgeo
- Dataset homepage: https://global-surface-water.appspot.com/
- STAC extensions used:
  - [Scientific](https://github.com/stac-extensions/scientific/)
  - [Projection](https://github.com/stac-extensions/projection/)


Global surface water products from the European Commission Joint Research Centre, based on Landsat 5, 7, and 8 imagery.  Layers in this collection describe the occurrence, change, and seasonality of surface water from 1984-2020.

## Usage

1. As a python module

```python
from stactools.jrc_gsw import stac, constants

# Create a STAC Collection
stac.create_collection(constants.CORE_JSC_GSW)

# Create a STAC Item
stac.create_item("/path/to/cog.tif")
```

2. Using the CLI

```bash
# STAC Collection
stac jrc-gsw create-collection -d "/path/to/output/directory"

# Create a STAC Item 
stac jrc-gsw create-item -d "/path/to/output/directory" -s "/path/to/input/cog.tiff"
```
