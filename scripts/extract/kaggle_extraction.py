# Extract data from Kaggle and create a dataset with the movies
import polars as pl
import kagglehub as kh
import boto3
import logging
from scripts import create_bucket as cb
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Load dataset from Kaggle and return a Polars LazyFrame
def load_dataset(dataset_name) -> pl.LazyFrame:
    path = kh.dataset_download(dataset_name)
    return pl.scan_csv(f"{path}/movies.csv")


# Create a new dataset with the movie titles and save it as a parquet file
def save_movie_titles_dataset(lf: pl.LazyFrame, output_path: str, storage_options: dict):
    lf.sink_parquet(
      output_path,
      storage_options=storage_options
    )

# General function to extract movie titles from the Kaggle dataset and save it to S3
def extract_and_save_movie_titles(dataset_name: str, output_path: str, s3, storage_options: dict):
    try:
        lf = load_dataset(dataset_name)

        bucket_name = output_path.replace("s3://", "").split("/")[0]
        cb.ensure_bucket_exists(bucket_name, s3)

        save_movie_titles_dataset(lf, output_path, storage_options)

        logger.info("Dataset with movie extracted and saved successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

# # Test
# if __name__ == "__main__":
#     import os
#     import boto3

#     s3 = boto3.client(
#         "s3",
#         endpoint_url="http://localhost:9000",
#         aws_access_key_id="admin",
#         aws_secret_access_key="admin123",
#     )

#     storage_options = {
#         "aws_access_key_id": "admin",
#         "aws_secret_access_key": "admin123",
#         "aws_endpoint_url": "http://localhost:9000",
#     }

#     dataset_name = "abdallahwagih/movies"
#     output_path = "s3://movies/bronze/movie_titles.parquet"

#     extract_and_save_movie_titles(dataset_name, output_path, s3, storage_options)

#     response = s3.list_objects_v2(Bucket="movies")

# import polars as pl
# import os

# df = pl.read_parquet(
#     "s3://movies/bronze/movie_titles.parquet",
#     storage_options={
#         "aws_access_key_id": "admin",
#         "aws_secret_access_key": "admin123",
#         "aws_endpoint_url": "http://localhost:9000",
#     }
# )

# print(df.head())
# print(df.shape)