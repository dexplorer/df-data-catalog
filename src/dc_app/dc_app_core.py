from metadata import dataset as ds
from metadata import dataset_dictionary as dd
from metadata import system_glossary as sg
from metadata import business_glossary as bg
from app_calendar import eff_date as ed
from dc_app.model import models as mm
import logging


def catalog_dataset(dataset_id: str, cycle_date: str) -> list:
    # Simulate getting the cycle date from API
    # Run this from the parent app
    if not cycle_date:
        cycle_date = ed.get_cur_cycle_date()

    # Simulate getting the dataset metadata from API
    logging.info("Reading the dataset metadata for dataset %s", dataset_id)
    dataset = ds.get_dataset_from_json(dataset_id=dataset_id)

    # Simulate getting the dataset dictionary metadata from API
    logging.info("Reading the dataset dictionary metadata for dataset %s", dataset_id)
    dataset_dict = dd.DatasetDictionary.from_json(dataset_id=dataset_id)

    # Simulate getting the system glossary metadata from API
    logging.info("Reading the system glossary")
    sys_glossary = sg.get_all_sys_glossary_items_from_json()

    # Simulate getting the business glossary metadata from API
    logging.info("Reading the business glossary")
    bus_glossary = bg.get_all_bus_glossary_items_from_json()

    asset_data_elements = []
    for column in dataset_dict.column_attributes:
        logging.info("Working on column %s", column.column_name)
        physical_data_element_name = column.column_name
        try:
            system_data_element_name = column.system_data_element_name
            if system_data_element_name:
                sys_glossary_item = lkp_sys_glossary(
                    system_data_element_name=system_data_element_name,
                    sys_glossary=sys_glossary,
                )
            else:
                raise ValueError("System data element name is not assigned for column")

            if sys_glossary_item:
                business_data_element_name = (
                    sys_glossary_item.business_data_element_name
                )
            else:
                raise ValueError("System glossary item is not found for column")

            if business_data_element_name:
                bus_glossary_item = lkp_bus_glossary(
                    business_data_element_name=business_data_element_name,
                    bus_glossary=bus_glossary,
                )

                if bus_glossary_item:
                    data_classification = bus_glossary_item.data_classification
                else:
                    raise ValueError("Business glossary item is not found for column")

                if not data_classification:
                    data_classification = mm.AssetDataClassType.OPEN.value

                if data_classification not in mm.AssetDataClassType:
                    raise ValueError("Data classification is not valid for column")
            else:
                logging.info(
                    "Business data element name is not found for column %s",
                    column.column_name,
                )

            asset_data_element = mm.AssetDataElement(
                physical_data_element_name=physical_data_element_name,
                system_data_element_name=system_data_element_name,
                business_data_element_name=business_data_element_name,
                data_classification=data_classification,
            )
            asset_data_elements.append(asset_data_element)

        except ValueError as error:
            print(physical_data_element_name)
            print(system_data_element_name)
            print(business_data_element_name)
            print(data_classification)
            logging.error(error)
            raise

    dc_asset = mm.Asset(
        asset_id=dataset_id.replace("dataset", "asset"),
        asset_type=dataset.dataset_type,
        asset_name=dataset.catalog_asset_name,
        asset_domain=dataset.catalog_asset_domain,
        asset_data_elements=asset_data_elements,
    )
    print(dc_asset)
    return dc_asset


def lkp_sys_glossary(
    system_data_element_name: str, sys_glossary: list[sg.SystemGlossaryItem]
) -> sg.SystemGlossaryItem:
    for item in sys_glossary:
        if item.system_data_element_name == system_data_element_name:
            return item
    return None


def lkp_bus_glossary(
    business_data_element_name: str, bus_glossary: list[bg.BusinessGlossaryItem]
) -> bg.BusinessGlossaryItem:
    for item in bus_glossary:
        if item.business_data_element_name == business_data_element_name:
            return item
    return None
