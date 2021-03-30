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

start = sys.argv[1]
end = sys.argv[2]

start_point = {start}
end_point = {end}
    
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

points = [el[0] for el in list_ready]
list_ready_dict = dict()

for el in list_ready:
    list_ready_dict[el[0]] = set(el[1][0])

list_ready_dict[end] = set([])

def bfs_paths(graph, start, goal):
    min_path = len(list_ready_dict)
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        if vertex in graph.keys() and len(path) <= min_path:
            for next in graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]
                    min_path = len(path)
                else:
                    queue.append((next, path + [next]))
                    
paths = bfs_paths(list_ready_dict, start, end)
result = list(paths)
result = sorted(result)

import pandas as pd
df = pd.DataFrame(result)
df.to_csv('LiliaMilutina_hw3_output', index=False, header=None)

from subprocess import PIPE, Popen
put = Popen(["hadoop", "fs", "-put", '-f', 'LiliaMilutina_hw3_output', sys.argv[4]], stdin=PIPE, bufsize=-1)
put.communicate()

sc.stop()

