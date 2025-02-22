import logging
import os

import click
from config.settings import ConfigParms as sc
from config import settings as scg
from dc_app import dc_app_core as dcc
from utils import logger as ufl

#
APP_ROOT_DIR = "/workspaces/df-data-catalog"


# Create command group
@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--dataset_id", type=str, default="dev", help="Source dataset id", required=True
)
@click.option("--env", type=str, default="dev", help="Environment")
@click.option("--cycle_date", type=str, default="", help="Cycle date")
def catalog_dataset(dataset_id: str, env: str, cycle_date: str):
    """
    Profile the dataset.
    """

    scg.APP_ROOT_DIR = APP_ROOT_DIR
    sc.load_config(env=env)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Start creating the catalog asset for the dataset %s", dataset_id)
    dc_asset = dcc.catalog_dataset(dataset_id=dataset_id, cycle_date=cycle_date)

    logging.info("Catalog asset for dataset %s", dataset_id)
    logging.info(dc_asset)

    logging.info("Finished creating the catalog asset for the dataset %s", dataset_id)


def main():
    cli()


if __name__ == "__main__":
    main()
