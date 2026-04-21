# Select only the movies titles from the movies dataset from Kaggle
import boto3
import polars as pl
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Open the parquet file with the movies dataset from Kaggle 
def open_kaggle_movies_dataset(s3_path, storage_options: dict):
    return pl.scan_parquet(
        s3_path,
        storage_options=storage_options
    )

# Filter only the movie titles from the dataset
def filter_movie_titles(lf: pl.LazyFrame):
    return lf.select("title").unique()

# Save the filtered movie titles dataset as a parquet file in S3
def save_filtered_movie_names(lf: pl.LazyFrame, output_path: str, storage_options: dict):
    lf.sink_parquet(
      output_path,
      storage_options=storage_options
    )

# General function to transform the movie titles dataset and save it to S3
def transform_movie_names(s3_input_path: str, s3_output_path: str, storage_options: dict):
    try:
        lf = open_kaggle_movies_dataset(s3_input_path, storage_options)
        filtered_lf = filter_movie_titles(lf)
        save_filtered_movie_names(filtered_lf, s3_output_path, storage_options)
        logger.info("Movie titles filtered and saved successfully.")

    except Exception as e:
        logger.error(f"Error in movie_titles_filter: {e}")

# # Testing
# if __name__ == "__main__":
#     s3_input_path = "s3://movies/bronze/movie_titles.parquet"
#     s3_output_path = "s3://movies/silver/only_movie_titles.parquet"

#     s3 = boto3.client(
#         "s3",
#         endpoint_url="http://localhost:9000",
#         aws_access_key_id="admin",
#         aws_secret_access_key="admin123",
#     )

#     storage_options = {
#         "aws_access_key_id": "admin",
#         "aws_secret_access_key": "admin123",
#         "aws_endpoint_url": "http://localhost:9000"
#      }
    
#     transform_movie_names(s3_input_path, s3_output_path, storage_options)
    