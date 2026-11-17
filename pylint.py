from collections import defaultdict
import boto3
#testing

def summarize_s3_by_date(bucket_name, prefix):
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")

    # Store file count and total bytes per date
    daily_stats = defaultdict(lambda: {"count": 0, "size_bytes": 0})

    print(f"Scanning s3://{bucket_name}/{prefix} ...\n")

    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if "Contents" not in page:
            continue

        for obj in page["Contents"]:
            # Skip directory placeholder keys (ending with '/')
            if obj["Key"].endswith("/"):
                continue

            # Extract YYYY-MM-DD from the LastModified timestamp (UTC)
            mod_date = obj["LastModified"].strftime("%Y-%m-%d")

            daily_stats[mod_date]["count"] += 1
            daily_stats[mod_date]["size_bytes"] += obj["Size"]

    if not daily_stats:
        print("No files found in the specified path.")
        return

    # Print formatted results sorted by date
    print(f"{'Date (UTC)':<15} | {'File Count':<12} | {'Total Size (MB)':<15}")
    print("-" * 48)

    for date_str in sorted(daily_stats.keys()):
        count = daily_stats[date_str]["count"]
        size_mb = daily_stats[date_str]["size_bytes"] / (1024 * 1024)
        print(f"{date_str:<15} | {count:<12} | {size_mb:<15.2f}")


if __name__ == "__main__":
    BUCKET = "test"
    PREFIX = "folder/"
    summarize_s3_by_date(BUCKET, PREFIX)
