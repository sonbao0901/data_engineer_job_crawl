import findspark

findspark.init()
findspark.find()

from pyspark.sql import SparkSession

spark = SparkSession\
                    .builder\
                    .appName("chat bot spark")\
                    .master("spark://localhost:7077")\
                    .config("spark.driver.host", "localhost")\
                    .getOrCreate()

df = spark.read.csv("test.csv", header=True, inferSchema=True)

df.show()