from jeeng.shared.clog import get_logger
import pickle
from google.cloud import storage


def list_objects(bucket_name: str, prefix: str) -> list[storage.blob]:
    files = []
    client = storage.Client()
    all_blobs = list(client.list_blobs(bucket_name, prefix=prefix + '/', delimiter='/'))

    for blob in all_blobs:
        if blob.name[-3:] == 'csv':
            files.append(blob)

    return files


def write_df_to_dbq(df,full_table_name):
    logger = get_logger("write_df_to_dbq")
    try:
        df.to_gbq(destination_table=full_table_name, project_id='jeeng-275018', if_exists='append')
    except Exception as exc:
        logger.error('gcs_utils.write_df_to_gcs', exc_info=True)


def store_pickle(obj,bucket,prefix,file_name):
    pkl_file = pickle.dumps(obj)
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = bucket.blob(prefix + '/' + file_name)
    gcs_writer = storage.blob.BlobWriter(blob)
    gcs_writer.write(pkl_file)
    gcs_writer.close()


def read_pickle(bucket,prefix,file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket)

    blob = bucket.blob(prefix + '/' + file_name )
    is_exists = blob.exists(client)
    if is_exists:
        obj = blob.download_as_bytes(client)
        pkl_obj = pickle.loads(obj)
        return pkl_obj
    else:
        return None
