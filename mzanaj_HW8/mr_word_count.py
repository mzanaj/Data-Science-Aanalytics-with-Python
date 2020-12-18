from mrjob.job import MRJob
import string
import re

#Read all lines 
WORD_RE = re.compile(r"[\w']+")

#Class
class mr_word_count(MRJob):
    #Read each word
    #Strip punctuation
    #Output: (key, value) word, 1
    def mapper(self, _, line):
        #All punctuation symbols 
        punct= string.punctuation
        #Loop in each word of the text 
        for word in WORD_RE.findall(line):
            my_word = str()
            #check each character
            for char in word:
                if(char in punct):
                    #Check if it is hyphen, if so consider them two different words (John's = "John" & "s")
                    if(char == "'"):
                        yield my_word.lower(),1
                    my_word= ''
                    continue
                else:
                    my_word = my_word +char
            #yield lower case
            yield my_word.lower(), 1
    #Key are coming from mapper (each word is a key, value = sum of all 1's that have same key)
    #All words that are identical be added and considered as one
    #I believe we have more than one key, meaning ( john:2, John: 2)
    def combiner(self, word, counts):
        yield word, sum(counts)
    #Reduce all: same key: will be reduced to one key
    def reducer(self, word, counts):
        yield word, sum(counts)
        
#Give control to cmd 
if __name__ == '__main__':
    mr_word_count.run()
