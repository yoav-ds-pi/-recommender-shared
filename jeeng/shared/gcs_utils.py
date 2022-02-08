import timeout_decorator

from jeeng.shared.clog import get_logger
import pickle
from google.cloud import storage

from jeeng.shared.time_mac import Timer


def list_objects(bucket_name: str, prefix: str) -> list[storage.blob]:
    files = []
    client = storage.Client()
    all_blobs = list(client.list_blobs(bucket_name, prefix=prefix + '/', delimiter='/', timeout=60))

    for blob in all_blobs:
        if blob.name[-3:] == 'csv':
            files.append(blob)

    return files


def write_df_to_dbq(df, full_table_name: str):
    logger = get_logger("write_df_to_dbq")

    @timeout_decorator.timeout(60)
    def do_write():
        df.to_gbq(destination_table=full_table_name, project_id='jeeng-275018', if_exists='append')

    try:
        logger.info(f'to_gbq {full_table_name=}')
        timer = Timer(f'{full_table_name=} to_gbq')
        do_write()
        logger.info(f'{timer.stop_round()}')
    except Exception:
        logger.error('gcs_utils.write_df_to_gcs', exc_info=True)


def store_pickle(obj, bucket_name: str, prefix: str, file_name: str):
    pkl_file = pickle.dumps(obj)
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(prefix + '/' + file_name)
    with storage.blob.BlobWriter(blob, timeout=60) as gcs_writer:
        gcs_writer.write(pkl_file)
    # gcs_writer.close()


def read_pickle(bucket_name: str, prefix: str, file_name: str):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(prefix + '/' + file_name)
    if blob.exists(client):
        obj = blob.download_as_bytes(client, timeout=60)
        pkl_obj = pickle.loads(obj)
        return pkl_obj
    return None
