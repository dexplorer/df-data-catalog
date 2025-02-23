# df-data-catalog

### Install

- **Install via Makefile and pip**:
  ```
    make install
  ```

### Usage Examples

- **Catalog a dataset via CLI**:
  ```sh
    dc-app-cli catalog-dataset --dataset_id "dataset_3" --env "dev"
  ```

- **Catalog a dataset via CLI with cycle date override**:
  ```sh
    dc-app-cli catalog-dataset --dataset_id "dataset_3" --env "dev" --cycle_date "2024-12-26"
  ```

- **Catalog a dataset via API**:
  ##### Start the API server
  ```sh
    dc-app-api --env "dev"
  ```
  ##### Invoke the API endpoint
  ```sh
    https://<host name with port number>/catalog-dataset/?dataset_id=<value>
    https://<host name with port number>/catalog-dataset/?dataset_id=<value>&cycle_date=<value>

    /catalog-dataset/?dataset_id=dataset_3
    /catalog-dataset/?dataset_id=dataset_3&cycle_date=2024-12-26
  ```
  ##### Invoke the API from Swagger Docs interface
  ```sh
    https://<host name with port number>/docs

  ```

### Sample Input (customers_20241226.csv)

```
effective_date,first_name,last_name,full_name,ssn,dob,street_addr1,street_addr2,city,state,country
2024-12-26,John,Connor,John Connor,987-65-4321,1988-05-03,155 North Blvd,,New York City,NY,USA
2024-12-26,Jill,Valentine,Jill Valentine,123-45-6789,1990-06-25,155 North Blvd,,Los Angeles,CA,USA
```

### API Data (simulated)
These are metadata that would be captured via the Metadata Management UI and stored in a database.

  ##### Datasets 
```
{
  "datasets": [
    {
      "dataset_id": "dataset_3",
      "dataset_type": "local delim file",
      "file_delim": ",",
      "file_path": "APP_DATA_IN_DIR/customers_yyyymmdd.csv",
      "schedule_id": "schedule_2",
      "recon_file_delim": "|",
      "recon_file_path": "APP_DATA_IN_DIR/customers_yyyymmdd.recon",
    }
  ]
}
```

  ##### Dataset Assets
```
{
  "dataset_id": "dataset_3",
  "catalog_asset_name": "Customer",
  "catalog_asset_domain": "Asset Management",
  "business_owners": ["Rajakumaran Arivumani"], 
  "technology_owners": ["Rajakumaran Arivumani"], 
  "data_stewards": ["Rajakumaran Arivumani"] 
}
```

  ##### Dataset Dictionary 
```
{
    "dictionaries": [
      {
        "dataset_id": "dataset_3",
        "column_attributes": [
          {
            "column_name": "effective_date",
            "column_description": "The date which represents the data snapshot that was effective as of this date.",
            "system_data_element_name": "Effective Date"
          },
          {
            "column_name": "first_name",
            "column_description": "Customer first name",
            "system_data_element_name": "Customer First Name"
          },
          {
            "column_name": "last_name",
            "column_description": "Customer last name",
            "system_data_element_name": "Customer Last Name"
          },
          {
            "column_name": "full_name",
            "column_description": "Customer full name",
            "system_data_element_name": "Customer Full Name"
          },
          {
            "column_name": "ssn",
            "column_description": "Customer's Social Security Number (SSN).",
            "system_data_element_name": "Customer SSN"
          },
          {
            "column_name": "dob",
            "column_description": "Customer's birth date",
            "system_data_element_name": "Customer DOB"
          },
          {
            "column_name": "street_addr1",
            "column_description": "Customer's home address - street address line 1",
            "system_data_element_name": "Customer Home Address - Street Address Line 1"
          },
          {
            "column_name": "street_addr2",
            "column_description": "Customer's home address - street address line 2",
            "system_data_element_name": "Customer Home Address - Street Address Line 2"
          },
          {
            "column_name": "city",
            "column_description": "Customer's home address - city",
            "system_data_element_name": "Customer Home Address - City"
          },
          {
            "column_name": "state",
            "column_description": "Customer's home address - state",
            "system_data_element_name": "Customer Home Address - State"
          },
          {
            "column_name": "country",
            "column_description": "Customer's home address - country",
            "system_data_element_name": "Customer Home Address - Country"
          }
        ]
      }
    ]
  }

```

  ##### System Glossary 
```
{
    "glossary_items": [
      {
        "system_data_element_name": "Effective Date",
        "system_data_element_description": "The date which represents the data snapshot that was effective as of this date.",
        "business_data_element_name": "As of Date"
      },
      {
        "system_data_element_name": "Asset Identifier",
        "system_data_element_description": "A unique identifier for the asset.",
        "business_data_element_name": ""
      },
      {
        "system_data_element_name": "Asset Type",
        "system_data_element_description": "A set of values that indicate the type of the asset.",
        "business_data_element_name": "Asset Type"
      },
      {
        "system_data_element_name": "Asset Name",
        "system_data_element_description": "This is the asset name.",
        "business_data_element_name": "Asset Name"
      },
      {
        "system_data_element_name": "Account Identifier",
        "system_data_element_description": "A unique identifier for the account.",
        "business_data_element_name": ""
      },
      {
        "system_data_element_name": "Asset Value in USD",
        "system_data_element_description": "This is the asset value in USD.",
        "business_data_element_name": "Asset Value in USD"
      },
      {
        "system_data_element_name": "Customer First Name",
        "system_data_element_description": "Customer first name",
        "business_data_element_name": "Customer First Name"
      },
      {
        "system_data_element_name": "Customer Last Name",
        "system_data_element_description": "Customer last name",
        "business_data_element_name": "Customer Last Name"
      },
      {
        "system_data_element_name": "Customer Full Name",
        "system_data_element_description": "Customer full name",
        "business_data_element_name": "Customer Full Name"
      },
      {
        "system_data_element_name": "Customer SSN",
        "system_data_element_description": "Customer's Social Security Number (SSN).",
        "business_data_element_name": "Customer SSN"
      },
      {
        "system_data_element_name": "Customer DOB",
        "system_data_element_description": "Customer's birth date",
        "business_data_element_name": "Customer DOB"
      },
      {
        "system_data_element_name": "Customer Home Address - Street Address Line 1",
        "system_data_element_description": "Customer's home address - street address line 1",
        "business_data_element_name": "Customer Home Address - Street Address Line 1"
      },
      {
        "system_data_element_name": "Customer Home Address - Street Address Line 2",
        "system_data_element_description": "Customer's home address - street address line 2",
        "business_data_element_name": "Customer Home Address - Street Address Line 2"
      },
      {
        "system_data_element_name": "Customer Home Address - City",
        "system_data_element_description": "Customer's home address - city",
        "business_data_element_name": "Customer Home Address - City"
      },
      {
        "system_data_element_name": "Customer Home Address - State",
        "system_data_element_description": "Customer's home address - state",
        "business_data_element_name": "Customer Home Address - State"
      },
      {
        "system_data_element_name": "Customer Home Address - Country",
        "system_data_element_description": "Customer's home address - country",
        "business_data_element_name": "Customer Home Address - Country"
      }
    ]
  }
```

  ##### Business Glossary 
```
{
    "glossary_items": [
      {
        "business_data_element_name": "As of Date",
        "business_data_element_description": "The date which represents the data snapshot that was effective as of this date.",
        "data_classification": ""
      },
      {
        "business_data_element_name": "Asset Type",
        "business_data_element_description": "A set of values that indicate the type of the asset.",
        "data_classification": ""
      },
      {
        "business_data_element_name": "Asset Name",
        "business_data_element_description": "This is the asset name.",
        "data_classification": ""
      },
      {
        "business_data_element_name": "Asset Value in USD",
        "business_data_element_description": "This is the asset value in USD.",
        "data_classification": ""
      },
      {
        "business_data_element_name": "Customer First Name",
        "business_data_element_description": "Customer first name",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer Last Name",
        "business_data_element_description": "Customer last name",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer Full Name",
        "business_data_element_description": "Customer full name",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer SSN",
        "business_data_element_description": "Customer's Social Security Number (SSN).",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer DOB",
        "business_data_element_description": "Customer's birth date",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer Home Address - Street Address Line 1",
        "business_data_element_description": "Customer's home address - street address line 1",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer Home Address - Street Address Line 2",
        "business_data_element_description": "Customer's home address - street address line 2",
        "data_classification": "PII"
      },
      {
        "business_data_element_name": "Customer Home Address - City",
        "business_data_element_description": "Customer's home address - city",
        "data_classification": ""
      },
      {
        "business_data_element_name": "Customer Home Address - State",
        "business_data_element_description": "Customer's home address - state",
        "data_classification": ""
      },
      {
        "business_data_element_name": "Customer Home Address - Country",
        "business_data_element_description": "Customer's home address - country",
        "data_classification": ""
      }
    ]
  }

```

### Sample Output 

```
{
  "results": {
    "asset_id": "asset_3",
    "asset_type": "local delim file",
    "asset_name": "Customer",
    "asset_domain": "Asset Management",
    "asset_data_elements": [
      {
        "physical_data_element_name": "effective_date",
        "system_data_element_name": "Effective Date",
        "business_data_element_name": "As of Date",
        "data_classification": "OPEN"
      },
      {
        "physical_data_element_name": "first_name",
        "system_data_element_name": "Customer First Name",
        "business_data_element_name": "Customer First Name",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "last_name",
        "system_data_element_name": "Customer Last Name",
        "business_data_element_name": "Customer Last Name",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "full_name",
        "system_data_element_name": "Customer Full Name",
        "business_data_element_name": "Customer Full Name",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "ssn",
        "system_data_element_name": "Customer SSN",
        "business_data_element_name": "Customer SSN",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "dob",
        "system_data_element_name": "Customer DOB",
        "business_data_element_name": "Customer DOB",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "street_addr1",
        "system_data_element_name": "Customer Home Address - Street Address Line 1",
        "business_data_element_name": "Customer Home Address - Street Address Line 1",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "street_addr2",
        "system_data_element_name": "Customer Home Address - Street Address Line 2",
        "business_data_element_name": "Customer Home Address - Street Address Line 2",
        "data_classification": "PII"
      },
      {
        "physical_data_element_name": "city",
        "system_data_element_name": "Customer Home Address - City",
        "business_data_element_name": "Customer Home Address - City",
        "data_classification": "OPEN"
      },
      {
        "physical_data_element_name": "state",
        "system_data_element_name": "Customer Home Address - State",
        "business_data_element_name": "Customer Home Address - State",
        "data_classification": "OPEN"
      },
      {
        "physical_data_element_name": "country",
        "system_data_element_name": "Customer Home Address - Country",
        "business_data_element_name": "Customer Home Address - Country",
        "data_classification": "OPEN"
      }
    ],
    "business_owners": [
      "Rajakumaran Arivumani"
    ],
    "technology_owners": [
      "Rajakumaran Arivumani"
    ],
    "data_stewards": [
      "Rajakumaran Arivumani"
    ]
  }
}

```