#Author: Habibi Husain Arifin
#Created Date: 15 January 2019
#Last Updated Date: 24 March 2021
#Version: 1.0

#<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

import math
import string

class Instance():
    insType = None
    gaGene = None
    parameters = None
    
    @staticmethod
    def getInstancesByType(insType, instances):
        #Reference: https://stackoverflow.com/questions/3013449/list-comprehension-vs-lambda-filter
        insts = list(filter(lambda inst:inst.insType == insType, instances))
        return insts
    
    @staticmethod
    def getInstanceByTypeAndGene(insType, gaGene, instances):
        insts = Instance.getInstancesByType(insType, instances)
        
        #Find the Instance for the Gene and return if can find
        for inst in insts:
            if inst.gaGene == gaGene:return inst
            
    @staticmethod
    def createNewInstance(insType, gaGene, parameters):
        inst = Instance()
        inst.gaGene = gaGene
        inst.insType = insType
        inst.parameters = parameters
        return inst
    
    #Calculate the number of characters of each gene based on MaxRowSize of the instance tables
    @staticmethod
    def getSizeOfGene(maxInstanceRow):
        sizeOfGene = 1 
        result = 0
        
        #The distance between A to Z (ASCII) is 26
        while result < 1:
            maxCandidate = math.pow(len(string.ascii_uppercase), sizeOfGene) #To calculate the maximum candidate based on the number of gene
            result = maxCandidate/maxInstanceRow
            if result < 1:sizeOfGene += 1 #if the result less than 1, means the size of gene cannot cover the number of components/rows
        
        return sizeOfGene
    
    #Generate the Genes sequentially and assign to the instances
    @staticmethod
    def generateGeneSequentially(instances, maxInstanceRow):
        #Get SizeOfGene based on the maximum number of candidate/possible components/instances 
        sizeOfGene = Instance.getSizeOfGene(maxInstanceRow)
        tempInstType = None
        tempIndex = 0
        
        #Looping every instance in the instance catalogs
        for instance in instances:
            #Check whether it is new type of Instance and reset the tempCounter if true to restart the Gene
            if instance.insType != tempInstType:    
                tempIndex = 0
            
            instance.gaGene = Instance.getGeneByIndex(tempIndex, sizeOfGene) #Assign GAGene with the gene based on index and the sizeOfGene
            tempIndex += 1 #Increase the tempCounter, so the gene know it will continue to the next ASCII character
            tempInstType = instance.insType #Replace the tempororary InstanceType to the new one
        
        return instances
    
    #Get gene sequentially based on the rowIndex and sizeOfGene
    @staticmethod
    def getGeneByIndex(index, sizeOfGene):
        gene = ""
        diff = index
        for i in reversed(range(0, sizeOfGene)): #Loop backward go start with the highest level of gene
            maxOfGene = math.pow(len(string.ascii_uppercase), i) #Calculate the value of each gene increament
            #print("digit", i+1, "maxOfGene", maxOfGene)
            mod = int(diff/maxOfGene) #Calculate the modulus of division of the current difference with the max value of the gene
            #print("mod", i+1, "mod", mod)
            gene += string.ascii_uppercase[mod] #Construct the gene
            diff -= (mod)*maxOfGene #Subtract the difference
        
        if gene != "":return gene
        else:return None
    
########################################################################################################################
#Below this line is test area
"""
#Test getSizeOfGene
geneSize = Instance.getSizeOfGene(500)
print("geneSize:", geneSize)
print("GetGeneByIndex", Instance.getGeneByIndex(675, geneSize))
"""
