from mrjob.job import MRJob
import string
import functools

import re
#Read all lines 

#Class
class mr_summary_stats(MRJob):
    
    def mapper(self, _, line):
        #Find all keys
        regex = re.compile(r"\d+\s")

        #Find all values
        regex2= re.compile(r"\s\-?\d+.\d+|\s\+?\d+.\d+")
        
        keys = [] 
        for x in regex.findall(line):
            keys.append(x)
        
        values = []    
        for y in regex2.findall(line):
            values.append(y)
            
        #Yield  population, [1, all x, x_squares]  
        for x in range(len(values)):
            pop = int(keys[x])
            all_x = float(values[x])
            all_x_square = float(values[x])*float(values[x])
            yield (pop,[1,all_x, all_x_square])
        #1 [1,2.0,4.0]
        #1 [1,3.0, 9.0], ...
    
    def reducer(self, keys,values):
       
        #1	[3, 6.0, 14.0]
        #2	[3, 0.0, 8.0]
        #3	[2, 20.0, 200.0]
        #keys, [pop[0], pop[1], pop[2]]
        
        pop= functools.reduce(lambda x,y:[x[0]+y[0], x[1]+y[1], x[2]+y[2]], values)

        n= pop[0]
        #mean, sum_x/n
        mean = pop[1]/n
        #var [sum(x^2) /n] - mean^2 (variance over n)
        var = (pop[2]/n)- (mean**2)

        yield (keys,tuple([n, mean, var]))

#Give control to cmd 
if __name__ == '__main__':
    mr_summary_stats.run()












