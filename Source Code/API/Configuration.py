#Author: Habibi Husain Arifin
#Created Date: 10 January 2019
#Last Updated Date: 24 March 2021
#Version: 1.0

#<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

import js2py
from API.StructureModel import XMI25Element
from API.Instance import Instance

#Tag Name
LOWER_VALUE = "lowerValue"
UPPER_VALUE = "upperValue"

#Stereotype
PART_PROPERTY = "PartProperty"
VALUE_PROPERTY = "ValueProperty"
CONSTRAINT_PARAMETER = "ConstraintParameter"
CONSTRAINT_BLOCK = "ConstraintBlock"
MOE = "MOE"

#Misc: Used internally only for this plugin
SOI = "SOI"
TOTAL = "total"
FITNESS_VALUE = "FitnessValue"
GA_GENE = "GAGene"

class Configuration():
    chromosomeSeq = None
    gaChromosome = None
    structureModel = None
    
    #Set the Gene of Catalog to XMI25Element
    @staticmethod
    def createNewConfiguration(structureModel, chromosome, instances):
        conf = Configuration() #Create new configuration
        conf.gaChromosome = chromosome #Set chromosome to the new configuration
        conf.chromosomeSeq = XMI25Element.getChromosomeSequence(structureModel)
        conf.structureModel = structureModel.copy() #Set the structure model
        tempCounter = 0 #This is to know the gene sequence in a chromosome

        #print("StructureModel", structureModel)
        #print("Chromosome", chromosome)
        #print("Instances", instances)
        
        #Set Gene to XMI25Element
        for el in conf.structureModel:
            elStereos = el.stereotypes
            
            #Set the Properties which are genes
            if elStereos != None and GA_GENE in elStereos:
                
                #The name of XMI25Element must same with the catalog sheet name, this is how we can find the correct catalogs/instances for the Property
                inst = Instance.getInstanceByTypeAndGene(el.typeXmi25Element.name, chromosome[tempCounter], instances)
                
                #Check whether the instance is not None/Null
                if inst != None:
                    #Set the gaGene of XMI25Element Gene
                    el.gaGene = inst.gaGene
                    
                    #Get the instanceParameters
                    instParams = inst.parameters
                    
                    #Set value to all ValueProperty
                    for vp in conf.structureModel:
                        if vp.stereotypes != None and VALUE_PROPERTY in vp.stereotypes:
                            
                            #Set Values to ValueProperty of XMI25Element Property which DefaultValue is not None/Null 
                            if vp.value != None:
                                XMI25Element.setValuesRecursively(vp, conf.structureModel, vp.value)
                            
                            else:
                                if vp.name in instParams.keys(): #To check whether the key is exist in the dictionary
                                    XMI25Element.setValuesRecursively(vp, conf.structureModel, instParams[vp.name], inst)
                                        
                else:
                    return None #The chromosome is invalid because one of the gene has not associated with any possible/candidate component
                
                tempCounter += 1 #Increase the counter so we will get the next gene in a chromosome
                inst = None #Empty the instance so it will be ready to be used for the next instance
        
        #Set the fitnessValue
        for fv in conf.structureModel:
            if fv.stereotypes != None and FITNESS_VALUE in fv.stereotypes:
                #print("Element is a FitnessValue", fv.name)
                
                #Check if fitnessValue is None. If it is None, calculate the value, else ignore it
                #if fv.value == None:
                fv = Configuration.calculateValueRecursively(fv, conf)
                #print("Set FitnessValue: ", fv.value)
            #else:
                #print("Element is Not a FitnessValue", fv.name)
        
        return conf
    
    #Calculate ValueRecursively
    @staticmethod
    def calculateValueRecursively(element, configuration):
        #print("\nStart calculateValueRecursively")
        bEls = XMI25Element.getChildrenElements(configuration.structureModel, element)
        
        #Find the Output ConstraintParameter
        if bEls != None:
            for bEl in bEls:
                if bEl.stereotypes != None:
                    if CONSTRAINT_PARAMETER in bEl.stereotypes:
                        if bEl.value == None: #if ConstraintParameter is None, find the constraintBlock
                            #print("Node 1_1:", bEl.nodeId, bEl.name, bEl.value)
                            bEl == Configuration.calculateConstraintRecursively(bEl, configuration)
                            XMI25Element.setValuesRecursively(bEl, configuration.structureModel, bEl.value)                            
                        #else:
                            #print("Node 1_2:", bEl.nodeId, bEl.name, bEl.value)
                    elif VALUE_PROPERTY in bEl.stereotypes: 
                        if bEl.value == None: #if ValueProperty is None, find the constraintParameter
                            #print("Node 1_3:", bEl.nodeId, bEl.name, bEl.value)
                            bEl == Configuration.calculateValueRecursively(bEl, configuration)
                            XMI25Element.setValuesRecursively(bEl, configuration.structureModel, bEl.value)   
                        #else:
                            #print("Node 1_4:", bEl.nodeId, bEl.name, bEl.value)
        #print("Stop calculateValueRecursively\n")
                
        return element
    
    #To calculate the value with constraintBlock recursively
    @staticmethod
    def calculateConstraintRecursively(element, configuration):
        #print("\nStart calculateConstraintRecursively")
        #Find the ConstraintBlock
        cBEls = XMI25Element.getChildrenElements(configuration.structureModel, element)
        
        if cBEls != None:
            for cBEl in cBEls:
                if cBEl.stereotypes != None and CONSTRAINT_BLOCK in cBEl.stereotypes:
                    #print("Node 2:", cBEl.name)

                    #Find the Input ConstraintParameters to calculate it
                    inPars = XMI25Element.getChildrenElements(configuration.structureModel, cBEl)
                    for inPar in inPars:
                        if inPar.value == None:
                            #print("Node 3_1:", inPar.nodeId, inPar.name, inPar.value)

                            #Get the Binded Element
                            inParBEls = XMI25Element.getChildrenElements(configuration.structureModel, inPar)
                            if inParBEls != None:
                                for inParBEl in inParBEls:
                                    if inParBEl.stereotypes != None and CONSTRAINT_PARAMETER in inParBEl.stereotypes:
                                        if inParBEl.value == None: #Calculate Recuversively if the value is None
                                            #print("Node 4_1:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                                            inParBEl = Configuration.calculateConstraintRecursively(inParBEl, configuration)
                                            
                                            if inParBEl.value != None:
                                                #print("Node 5_1:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                                                XMI25Element.setValuesRecursively(inParBEl, configuration.structureModel, inParBEl.value)
                                            #else:
                                                #print("Node 5_2:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                                                
                                        else:
                                            #print("Node 4_2:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                                            XMI25Element.setValuesRecursively(inParBEl, configuration.structureModel, inParBEl.value)
                                                                               
                                    elif inParBEl.stereotypes != None and VALUE_PROPERTY in inParBEl.stereotypes:
                                        if inParBEl.value == None:
                                            #print("Node 4_3:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                                            inParBEl = Configuration.calculateValueRecursively(inParBEl, configuration)
                                            if inParBEl.value == None: 
                                                #print("Node 5_3:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                                                
                                                #The childrenElements cannot be found, then find the original ValueProperty
                                                sameEls = XMI25Element.getElementByXmiId(configuration.structureModel, inParBEl.xmiId)
                                                if sameEls != None:
                                                    for sameEl in sameEls:
                                                        if sameEl.value == None:
                                                            #print("Node 6_1:", sameEl.nodeId, sameEl.name, sameEl.value)
                                                            sameEl = Configuration.calculateValueRecursively(sameEl, configuration)
                                                            XMI25Element.setValuesRecursively(sameEl, configuration.structureModel, sameEl.value)
                                                        else:
                                                            #print("Node 6_2:", sameEl.nodeId, sameEl.name, sameEl.value)
                                                            XMI25Element.setValuesRecursively(sameEl, configuration.structureModel, sameEl.value)
                                            else:
                                                #The childrenElements can be found, set the Values
                                                #print("Node 5_4:", inParBEl.nodeId, inParBEl.name, inParBEl.value)               
                                                XMI25Element.setValuesRecursively(inParBEl, configuration.structureModel, inParBEl.value)
                                                
                                                #Find the same element
                                                sameEls = XMI25Element.getElementByXmiId(configuration.structureModel, inParBEl.xmiId)
                                                if sameEls != None:
                                                    for sameEl in sameEls:
                                                        if sameEl.value == None:
                                                            #print("Node 6_3:", sameEl.nodeId, sameEl.name, sameEl.value)
                                                            sameEl = Configuration.calculateValueRecursively(sameEl, configuration)
                                                            XMI25Element.setValuesRecursively(sameEl, configuration.structureModel, sameEl.value)
                                                        else:
                                                            #print("Node 6_4:", sameEl.nodeId, sameEl.name, sameEl.value)
                                                            XMI25Element.setValuesRecursively(sameEl, configuration.structureModel, sameEl.value)
                                        
                                        #else:
                                        #    print("Node 4_4:", inParBEl.nodeId, inParBEl.name, inParBEl.value)
                        #else:
                        #    print("Node 3_2:", inPar.nodeId, inPar.name, inPar.value)
                            
                        #Run the JavaScript
                        if Configuration.isCompletedParameters(inPars):
                            element.value = Configuration.executeJs(element, inPars, cBEl.formula)  
             
        #print("Stop calculateConstraintRecursively\n")

        return element
    
    #To check whether any of Input ConstraintParameters is None
    @staticmethod
    def isCompletedParameters(inputParams):     
        for inputParam in inputParams:           
            if inputParam.value == None:return False #return False immediately if found any None inputParameter
        return True
    
    #Run JavaScript
    @staticmethod
    def executeJs(outPar, inPars, formula):
        func = "function calculate(){"
        
        #Construct the Parameters
        pars = "\nvar " + outPar.name
        for inPar in inPars:
            pars += ", " + inPar.name  
        for inPar in inPars:
            pars += "\n" + inPar.name + " = " + str(inPar.value)
        pars += "\n"
         
        form = formula
        result="\nreturn " + outPar.name + "}" #outPar.name
        callFunc="\ncalculate()"
        
        #Construct the JavaScript
        js = func + pars + formula + result + callFunc
        #print("\n", js) #Debug the JavaScript

        result = js2py.eval_js(js)  # executing JavaScript and converting the result to python string 
        #print(outPar.name, ":", result) #Print result
        return result
        
    #Get the fitnessValue from the configuration, if it is None, then calculate it first
    @staticmethod
    def getFitnessValue(configuration):
        if configuration != None:
            for el in configuration.structureModel:
                elStereos = el.stereotypes
                if elStereos != None and FITNESS_VALUE in elStereos:
                    if el.value != None:return el.value
                    else:return 0
        else:return 0


########################################################################################################################
#Below this line is test area
"""
chromosome = ["A", "B", "A", "A", "A"]
newConf = Configuration.createNewConfiguration(structModel, chromosome, instances)

if newConf != None:
    print("chromosome:", newConf.chromosomeSeq, newConf.gaChromosome, "\n")
    for obj in newConf.structureModel:
        if obj.stereotypes != None:
            if VALUE_PROPERTY in obj.stereotypes or CONSTRAINT_PARAMETER in obj.stereotypes:
                print(Colors.getFontColorByLevel(obj.level), Colors.BOLD, XPathHelper.getRepeatedChar("\t", obj.level), obj.stereotypes, "LV.", obj.level, Colors.ENDC, ", gene =", obj.gaGene, ", nId =", obj.nodeId, ", name =", obj.name, ", value =", obj.value)
            elif CONSTRAINT_BLOCK in obj.stereotypes:
                print(Colors.getFontColorByLevel(obj.level), Colors.BOLD, XPathHelper.getRepeatedChar("\t", obj.level), obj.stereotypes, "LV.", obj.level, Colors.ENDC, ", gene =", obj.gaGene, ", nId =", obj.nodeId, ", name =", obj.name, ", formula =", obj.formula)
            else:
                print(Colors.getFontColorByLevel(obj.level), Colors.BOLD, XPathHelper.getRepeatedChar("\t", obj.level), obj.stereotypes, "LV.", obj.level, Colors.ENDC, ", gene =", obj.gaGene, ", nId =", obj.nodeId, ", name =", obj.name)
    print("\nNo. of element:", len(newConf.structureModel), "DateTime:", str(DT.datetime.now()))
else:
    print("The chromosome is invalid because one of the gene has not associated with any possible/candidate component:", newConf)
"""
