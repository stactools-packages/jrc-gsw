import stactools.core

from stactools.jrc_gsw import constants, stac

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.jrc_gsw import commands

    registry.register_subcommand(commands.create_jrc_gsw_command)


__all__ = [constants, stac]
__version__ = "0.1.0"
"""Library version"""
