from womboGeneration import wombo
import csv
import codecs

def readTabforWombo(filename):
    with open(filename) as womboDirections:
        ## Saved files with Tabs to make it easier to deal with commas
        reader = csv.DictReader(womboDirections, delimiter='\t')
    
        for dir in reader:
            
            if dir['Style'] != 'Done' and len(dir['Summary']) > 0:
                wombo(dir['Summary'], dir['Style'], dir['Genre'])


if __name__ == "__main__":
    readTabforWombo('mytsv.txt')


