"""File system paths and storage locations"""

# S3 Configuration
S3_BUCKET = "synpuf-omop"
S3_BASE_PATH = f"s3a://{S3_BUCKET}"


# OMOP Table Paths
OMOP_TABLES = {
    "person": f"{S3_BASE_PATH}/person/",
    "visit_occurrence": f"{S3_BASE_PATH}/visit_occurrence/",
    "condition_occurrence": f"{S3_BASE_PATH}/condition_occurrence/",
    "procedure_occurrence": f"{S3_BASE_PATH}/procedure_occurrence/",
    "drug_exposure": f"{S3_BASE_PATH}/drug_exposure/",
    "measurement": f"{S3_BASE_PATH}/measurement/",
    "observation": f"{S3_BASE_PATH}/observation/"
}


# Delta Lake paths (for saving transformed data)
DELTA_BASE_PATH = "/user/hive/warehouse/omop_warehouse"