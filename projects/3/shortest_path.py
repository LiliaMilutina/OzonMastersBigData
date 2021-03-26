import os
import sys

SPARK_HOME = "/usr/hdp/current/spark2-client"
PYSPARK_PYTHON = "/opt/conda/envs/dsenv/bin/python"
os.environ["PYSPARK_PYTHON"]= PYSPARK_PYTHON
os.environ["SPARK_HOME"] = SPARK_HOME

PYSPARK_HOME = os.path.join(SPARK_HOME, "python/lib")
sys.path.insert(0, os.path.join(PYSPARK_HOME, "py4j-0.10.7-src.zip"))
sys.path.insert(0, os.path.join(PYSPARK_HOME, "pyspark.zip"))

import random
from pyspark import SparkContext, SparkConf
spark_ui_port = random.choice(range(10000, 11000))
print(f"Spark UI port: {spark_ui_port}")

conf = SparkConf()
conf.set("spark.ui.port", spark_ui_port)

sc = SparkContext(appName="hw3", conf=conf)

from pyspark.accumulators import AccumulatorParam

class SetParam(AccumulatorParam):
    def zero(self,  value = ""):
        return set()

    def addInPlace(self, value1, value2):
        value1.update(value2)
        return value1
    
def iteration_process(element, to_visit_ids, distance):
    global to_visit_ids_accu
    global found_target
    global hero_id_target_broadcast
    
    id = element[0]
    visited = element[1][1][1]

    if (visited is False) and (id in to_visit_ids):
        
        if id == hero_id_target_broadcast.value:
            found_target += 1
        visited = True
        to_visit_ids_accu.add(set(element[1][0]))
        
        return (id, (element[1][0], (distance, True)))

    return (id, (element[1][0], (distance, visited)))

raw_graph = sc.textFile(sys.argv[3])

graph = raw_graph.map(lambda x: x.split("\t")[::-1]).cache()

vertices = graph.map(lambda x: x[0]).union(graph.map(lambda x: x[1])).distinct()
num_vertices = vertices.count()
info = vertices.map(lambda x: (x, (num_vertices, False)))
links = graph.groupByKey().mapValues(list).cache()
rdd = links.join(info)

start_point = {sys.argv[1]}
end_point = {sys.argv[2]}
    
to_visit_ids_accu = sc.accumulator(set(), SetParam())
found_target = sc.accumulator(0)
hero_id_target_broadcast = sc.broadcast(end_point)
to_visit_ids_accu.add(start_point)

distance = 0

while True:
    to_visit_ids = to_visit_ids_accu.value

    if len(to_visit_ids) == 0:
        break
        
    to_visit_ids_accu = sc.accumulator(set(), SetParam())

    rdd = rdd.map(lambda x: iteration_process(x, to_visit_ids, distance))

    rdd.persist()

    rdd.count()
        
    if found_target.value > 0:
        break

    distance += 1
    
list_ready = rdd.filter(lambda x: x[1][1][1] == True)
list_ready = list_ready.collect()
point = start_point.pop()
points = [el[0] for el in list_ready]
list_ready_dict = dict()

for el in list_ready:
    list_ready_dict[el[0]] = el[1][0]
    
list_ready_dict[end_point.pop()] = []

def bfs(graph, start, end):

    queue = []
    queue.append([start])
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            return path

        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)
    
result = bfs(list_ready_dict, start_point.pop(), end_point.pop())
res = [int(el) for el in result]


import csv
file = open(sys.arv[4], "w")
writer = csv.writer(file, delimiter = ",")
writer.writerow(res)
file.close()
