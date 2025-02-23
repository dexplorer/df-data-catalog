from enum import StrEnum, Flag, auto
from dataclasses import dataclass
import ast

# This is the same as DatasetType enum
class AssetType(StrEnum):
    GENERIC = 'generic'
    DELIM_FILE = 'delim file'
    LOCAL_DELIM_FILE = 'local delim file'
    AWS_S3_DELIM_FILE = 'aws s3 delim file'
    AZURE_ADLS_DELIM_FILE = 'azure adls delim file'
    SPARK_TABLE = 'spark table'
    SPARK_SQL_FILE = 'spark sql file'

class AssetDataClassType(StrEnum):
    OPEN = 'OPEN'
    PII = 'PII'
    SENSITIVE = 'SENSITIVE'
    # RESTRICTED = 'RESTRICTED'

class AssetDataClassTypeFlag(Flag):
    PII = auto()
    SENSITIVE = auto()
    RESTRICTED = PII | SENSITIVE
    OPEN = ~RESTRICTED

@dataclass
class AssetDataElement:
    physical_data_element_name: str
    system_data_element_name: str
    business_data_element_name: str 
    data_classification: AssetDataClassType

@dataclass
class Asset:
    asset_id: str
    asset_type: AssetType 
    asset_name: str
    asset_domain: str
    asset_data_elements: list[AssetDataElement]
    business_owners: list[str]
    technology_owners: list[str]
    data_stewards: list[str]

    def __init__(
        self,
        asset_id: str,
        asset_type: AssetType,
        asset_name: str,
        asset_domain: str,
        asset_data_elements: list[AssetDataElement] | list[dict],
        business_owners: list[str], 
        technology_owners: list[str], 
        data_stewards: list[str]
    ):
        self.asset_id = asset_id
        self.asset_type = asset_type
        self.asset_name = asset_name
        self.asset_domain = asset_domain
        if isinstance(asset_data_elements, list) and all(
            isinstance(asset_data_element, dict) for asset_data_element in asset_data_elements
        ):
            self.asset_data_elements = [
                AssetDataElement(**asset_data_element)
                for asset_data_element in asset_data_elements
            ]
        else:
            self.asset_data_elements = asset_data_elements
        self.business_owners = business_owners
        self.technology_owners = technology_owners
        self.data_stewards = data_stewards
