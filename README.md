# stactools jrc-gsw

Collection of tools for working with STAC and the [Global Surface Water dataset](https://global-surface-water.appspot.com/download) produced by the [Joint Research Centre](https://ec.europa.eu/info/departments/joint-research-centre_en).

This dataset "...maps the location and temporal distribution of water surfaces at the global scale over the past 3.7 decades, and provides statistics on their extent and change to support better informed water-management decision-making."

## Usage

1. As a python module

```python
from stactools.jrc-gsw.constants import JSONLD_HREF
from stactools.jrc-gsw import utils, cog, stac


# Read metadata
metadata = utils.get_metadata(JSONLD_HREF)

# Create a STAC Collection
json_path = os.path.join(tmp_dir, "/path/to/jrc-gsw.json")
stac.create_collection(metadata, json_path)

# Create a COG
cog.create_cog("/path/to/local.tif", "/path/to/cog.tif")

# Create a STAC Item
stac.create_item(metadata, "/path/to/item.json", "/path/to/cog.tif")
```

2. Using the CLI

```bash
# STAC Collection
stac jrc-gsw create-collection -d "/path/to/directory"
# Create a COG - creates /path/to/local_cog.tif
stac jrc-gsw create-cog -d "/path/to/directory" -s "/path/to/local.tif"
# Create a STAC Item - creates /path/to/directory/local_cog.json
stac jrc-gsw create-item -d "/path/to/directory" -c "/path/to/local_cog.tif"
```
