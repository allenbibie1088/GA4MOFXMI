#Author: Habibi Husain Arifin
#Created Date: 10 January 2019
#Last Updated Date: 24 March 2021
#Version: 1.0

#<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

import random
import string
import copy
from strgen import StringGenerator
from deap import base, creator, tools, algorithms
from API.Configuration import Configuration

class GeneticAlgorithms():
 
    @staticmethod
    def generateGeneRandomly(k=1):
        gene = None
        lowerBound = string.ascii_uppercase[0]
        upperBound = string.ascii_uppercase[-1]
        template = "[" + lowerBound + "-" + upperBound + "]{" + str(k) + "}"
        gene = StringGenerator(template).render()
        return gene
    
    #Get permitted gene from the instance based on type
    @staticmethod
    def getPermittedGenes(instType, instances):
        permGenes = []
        for inst in instances:
            if inst.insType == instType:permGenes.append(inst.gaGene)
        
        if permGenes != []:return permGenes
        else:return None
    
    #Tool decoration is a very powerful feature that helps to control very precise things during an evolution
    #without changing anything in the algorithm or operators.
    #Reference: https://deap.readthedocs.io/en/master/tutorials/basic/part2.html
    @staticmethod
    def checkExistence(chromosomeSeq, instances):
        def decorator(func):
            def wrapper(*args, **kargs):
                offspring = func(*args, **kargs)
                #print("Original offspring:", offspring) #Debug before check PermittedGenes
                for child in offspring:
                    for i in range(len(child)):
                        
                        #Get the permitted genes from the catalog of instances
                        permGenes = GeneticAlgorithms.getPermittedGenes(chromosomeSeq[i], instances)
                        #print("Permitted genes:", chromosomeSeq[i], permGenes) #Debug the PermittedGenes
                        
                        #If not exist in the InstanceCatalog, replace the gene/component with new random component
                        if child[i] not in permGenes:child[i] = child[i].replace(child[i], random.choice(permGenes))
                
                #print("Altered offspring:", offspring) #Debug after check PermittedGenes
                return offspring
            return wrapper
        return decorator
    
    @staticmethod
    def evaluation(chromosome, structureModel=None, instances=None):
        sm = copy.deepcopy(structureModel)
        conf = Configuration.createNewConfiguration(sm, chromosome, instances) #Create newConfiguration
        if conf != None:print("Evaluate chromosome:", chromosome)
        else:print("Cannot evaluate chromosome, one or more chromosome(s) is out of bound:", chromosome)
        fitness = Configuration.getFitnessValue(conf) #Get theFitnessValue
        return fitness,
    
    #Reference: https://deap.readthedocs.io/en/master/overview.html
    @staticmethod
    def customEvolution(popSize, noOfGeneration, toolbox):
        pop = toolbox.population(n=popSize)
        CXPB, MUTPB, NGEN = 0.5, 0.2, noOfGeneration

        # Evaluate the entire population
        fitnesses = map(toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        for g in range(NGEN):
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))
            
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                #print(child1, child2)
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
                
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # The population is entirely replaced by the offspring
            pop[:] = offspring
            #print(pop)

        return pop
