import argparse
import typing

import boto3
from terminaltables import GithubFlavoredMarkdownTable

from abstractions.bucket_stats import BucketStats
from abstractions.display_converter import DisplayConverter

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--conversion', type=str, help='convert total byte size. optional, but must be one of ki, Mi, Gi')



def get_s3_resource():
    return boto3.resource('s3')


def get_s3_stats(s3) -> typing.Sequence[BucketStats]:
    """
    iterate through all buckets and create BucketStats
    :param s3: s3 connection
    :return: List[BucketStats]
    """
    return [get_bucket_stats(bucket) for bucket in s3.buckets.all()]


def get_bucket_stats(bucket) -> BucketStats:
    """
    create individual BucketStats
    :param bucket: s3.Bucket
    :return: BucketStats
    """
    bucket_creation_date = bucket.creation_date
    bucket_last_modified = bucket_creation_date
    bucket_stats = BucketStats(bucket.name, bucket_creation_date, bucket_last_modified)
    for obj in bucket.objects.all():
        bucket_stats.update(obj)

    return bucket_stats

def create_table(conversion: str, s3_stats: typing.Sequence[BucketStats]) -> GithubFlavoredMarkdownTable:
    """
    creates final display table
    :param conversion: convert to ki, Mi and Gi
    :param s3_stats: List[BucketStats] calculated from get_bucket_stats
    """
    converter = DisplayConverter(conversion)
    header = [field for field in s3_stats[0].fields]
    table_data = [header]
    for stats in s3_stats:
        table_row = [str(value) if key != 'total_file_size' else str(converter.convert(value)) \
                         for key, value in zip(header, stats.props)]
        table_data.append(table_row)
    return GithubFlavoredMarkdownTable(table_data)

if __name__ == '__main__':
    args = parser.parse_args()
    s3 = get_s3_resource()
    s3_stats = get_s3_stats(s3)
    print(create_table(args.convert, s3_stats).table)


