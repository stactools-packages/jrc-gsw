ARG STACTOOLS_VERSION=latest
FROM stacutils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/stactools-jrc-gsw

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml setup.cfg ./
COPY src/stactools/jrc_gsw/__init__.py src/stactools/jrc_gsw/
RUN pip install . \
    && rm -r /opt/conda/lib/python3.8/site-packages/stactools/jrc_gsw

COPY src ./src
RUN pip install .
