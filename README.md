# Project
## Question 1
How did changing values on the SparkSession property parameters affect the throughput and latency of the data?

Changing for example these properties in the SparkSession below

- spark.sql.shuffle.partitions
- spark.default.parallelism

either increase or decrease the throughput and latency depending on job algorithm, size of data, machine resources, and so on ..

## Question 2
What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

Through checking two indicies inputRowsPerSecond and processedRowsPerSecond, it is concluded that these two key/value pairs are the best
- "spark.default.parallelism": "2"
- "spark.sql.shuffle.partitions": "1"
