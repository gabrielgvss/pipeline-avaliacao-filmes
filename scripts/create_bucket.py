import logging
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create an S3 bucket if it doesn't exist
def create_bucket(bucket_name: str, s3):
    try:
        s3.create_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' created successfully.")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            logger.info(f"Bucket '{bucket_name}' already exists (race condition).")
        else:
            logger.error(f"Error creating bucket: {e}")
            raise

# Check if a bucket exists and create it if it doesn't
def ensure_bucket_exists(bucket_name: str, s3):
    try:
        s3.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket '{bucket_name}' already exists.")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code in ("404", "NoSuchBucket"):
            logger.info(f"Bucket '{bucket_name}' does not exist. Creating it...")
            create_bucket(bucket_name, s3)

        else:
            logger.error(f"Error accessing bucket: {e}")
            raise