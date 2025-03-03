import os
import logging
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from dc_app import dc_app_core as dcc
from dc_app.discover import query as dcdq
from utils import logger as ufl
from utils import json_io as ufj

from fastapi import FastAPI
import uvicorn

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
    Create catalog asset for the dataset.

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

    all_assets_data_file_path = f"{sc.data_out_file_path}/assets.json"
    ufj.uf_merge_json_files(
        in_file_dir_path=sc.data_out_file_path,
        out_file=all_assets_data_file_path,
        in_file_pattern="asset_*",
    )

    logging.info("Finished creating the catalog asset for the dataset %s", dataset_id)

    return {"results": dc_asset}


@app.get("/query-catalog/")
async def query_catalog():
    """
    Query catalog.

    Args:
        none

    Returns:
        Physical asset and data element names.
    """

    logging.info("Start querying the catalog")
    response = dcdq.query_catalog(
        all_assets_data_file_path="/workspaces/df-data-catalog/data/out/assets.json"
    )
    logging.info("Finished querying the catalog")

    return {"response": response}


def main():
    # Load the environment variables from .env file
    load_dotenv()
    logging.info(os.environ)

    # Fail if env variable is not set
    sc.env = os.environ["ENV"]
    sc.app_root_dir = os.environ["APP_ROOT_DIR"]
    sc.load_config()

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
