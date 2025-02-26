import logging
import os

# from dotenv import load_dotenv
import click
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from config import settings as scg
from dc_app import dc_app_core as dcc
from dc_app.discover import query as dcdq
from utils import logger as ufl
from utils import json_io as ufj

#
# APP_ROOT_DIR = "/workspaces/df-data-catalog"

# Load the environment variables from .env file
load_dotenv()
logging.info(os.environ)
# Fail if APP_ROOT_DIR env variable is not set
APP_ROOT_DIR = os.environ["APP_ROOT_DIR"]


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
    Create catalog asset the dataset.
    """

    scg.APP_ROOT_DIR = APP_ROOT_DIR
    sc.load_config(env=env)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")
    logging.info(os.environ)

    logging.info("Start creating the catalog asset for the dataset %s", dataset_id)
    asset_data_file_path = f"{sc.data_out_file_path}/asset_{dataset_id}.json"
    dc_asset = dcc.catalog_dataset(
        dataset_id=dataset_id,
        cycle_date=cycle_date,
        asset_data_file_path=asset_data_file_path,
    )

    logging.info("Catalog asset for dataset %s", dataset_id)
    logging.info(dc_asset)

    all_assets_data_file_path = f"{sc.data_out_file_path}/assets.json"
    ufj.uf_merge_json_files(
        in_file_dir_path=sc.data_out_file_path,
        out_file=all_assets_data_file_path,
        in_file_pattern="asset_*",
    )

    logging.info("Finished creating the catalog asset for the dataset %s", dataset_id)


@cli.command()
def query_catalog():
    """
    Query catalog.
    """

    response = dcdq.query_catalog(
        all_assets_data_file_path="/workspaces/df-data-catalog/data/out/assets.json"
    )
    print(response)


def main():
    cli()


if __name__ == "__main__":
    main()
