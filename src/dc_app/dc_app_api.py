import os
import argparse
import logging

from config.settings import ConfigParms as sc
from config import settings as scg
from dc_app import dc_app_core as dcc
from utils import logger as ufl

from fastapi import FastAPI
import uvicorn

#
APP_ROOT_DIR = "/workspaces/df-data-catalog"

app = FastAPI()


@app.get("/")
async def root():
    """
    Default route

    Args:
        none

    Returns:
        A default message.
    """

    return {"message": "Data Catalog App"}


@app.get("/catalog-dataset/")
async def catalog_dataset(dataset_id: str, cycle_date: str = ""):
    """
    Catalog the dataset.

    Args:
        dataset_id: Id of the dataset.
        cycle_date: Cycle date

    Returns:
        Data catalog asset definition for the dataset.
    """

    logging.info("Start creating the catalog asset for the dataset %s", dataset_id)
    asset_data_file_path = f"{sc.data_out_file_path}/asset_{dataset_id}.json"
    dc_asset = dcc.catalog_dataset(
        dataset_id=dataset_id,
        cycle_date=cycle_date,
        asset_data_file_path=asset_data_file_path,
    )
    logging.info("Finished creating the catalog asset for the dataset %s", dataset_id)

    return {"results": dc_asset}


def main():
    parser = argparse.ArgumentParser(description="Data Catalog Application")
    parser.add_argument(
        "-e", "--env", help="Environment", const="dev", nargs="?", default="dev"
    )

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    env = args["env"]

    scg.APP_ROOT_DIR = APP_ROOT_DIR
    sc.load_config(env=env)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Starting the API service")

    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.cfg_file_path}/api_log.ini",
    )

    logging.info("Stopping the API service")


if __name__ == "__main__":
    main()
