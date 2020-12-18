#Question 3
#1. 
from pyspark import SparkConf, SparkContext
import sys

# This script takes two arguments, an input and output
if len(sys.argv) != 3:
  print('Usage: ' + sys.argv[0] + ' <in> <out>')
  sys.exit(1)

inputlocation = sys.argv[1]
outputlocation = sys.argv[2]

# Set up the configuration and job context
conf = SparkConf().setAppName('magic')
sc = SparkContext(conf=conf)


# Read in the dataset and immediately transform all the lines in array
data= sc.textFile(inputlocation).map(lambda line: line.split())

#Find all possible combinations
def all_possible_friends(line):
    l2=[]
    for x in line[1:]:
        l2.append(int(x))
    
    t  = []
    n = (len(l2)-1)
    p = 1
    
    for x in range(len(l2)-1):
        c = p
        for y in range(n):
            
            #actual combinations
            komb0 = (int(line[0]),int(l2[x]),int(l2[c]))
            komb= (tuple(sorted(komb0)))
            map_komb= (komb,1)
            t.append(map_komb)
            c= c+1
        n = n-1
        p = p+1
    #print(sorted(t))    
    return t


#Map and reduce
data = data.flatMap(all_possible_friends)
data = data.reduceByKey(lambda x,y: x+y)

#Filter only friends with 2 edges (>1)
filter_data = data.filter(lambda x:x[1]>1)

#Map by key 
final_data = filter_data.map(lambda x:x[0])

#Save
final_data.saveAsTextFile(outputlocation)

#Terminate session
sc.stop()