import os
import shutil
import sh
import subprocess
from pyspark.sql.functions import *


# File path / Hadoop Directory 
directory = '/user/ivy2/Tweets/'
file = '*.json'
path = directory + file

# Parse JSON into Spark dataframe
tweets_df = spark.read.json(path)

# Column Selection
tweets_df_l1 = tweets_df.select("id", "lang", "created_at", "user.screen_name", "user.location", "text")#.limit(10000)

# Match tweets referring directly to University of Chicago (University of Chicago)
# Much more refined search can go in this part
tweets_df_l2 = tweets_df_l1.where("lower(text) like '%uchicago%' or lower(text) like '%uofc%'")

# Remove newlines etc.
tweets_df_l3 = tweets_df_l2.withColumn("text_clean", regexp_replace("text", "[\\r\\n\\t]", " "))

# Drop original text column for reworked one
tweets_df_l4 = tweets_df_l3.drop('text')

# write to file
tweets_df_l4.write.format("com.databricks.spark.csv").option("header", "false").option("delimiter", "\t").save("hdfs:///user/orestalickolli/twitter_out")

