#Author: Habibi Husain Arifin
#Created Date: 10 January 2019
#Last Updated Date: 12 February 2020
#Version: 1.0
#<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

import matplotlib.pyplot as plt
import networkx as nx
import pydot

#Stereotype
PART_PROPERTY = "PartProperty"
VALUE_PROPERTY = "ValueProperty"
CONSTRAINT_PARAMETER = "ConstraintParameter"
CONSTRAINT_BLOCK = "ConstraintBlock"
MOE = "MOE"

#Misc: Used internally only for this plugin
FITNESS_VALUE = "FitnessValue"
GA_GENE = "GAGene"
SOI = "SOI"

class RNLTree:
    @staticmethod
    def drawGraph(structureModel):
        g = nx.Graph()

        for obj in structureModel:
            g.add_node(obj.nodeId, level=obj.level)
            if obj.parentNodeId != None:
                g.add_edge(obj.nodeId, obj.parentNodeId, rel=obj.relationship)

        pos = nx.nx_pydot.graphviz_layout(g, prog="dot")

        plt.figure(figsize=(50,50))
        nx.draw_networkx_nodes(g, pos, node_size=900, node_color="w")
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_edge_labels(g, pos, font_color="r")
        plt.axis("off")
        plt.show()
        
    def drawSimplifiedGraph(structureModel, root):
        g = nx.Graph()

        for obj in structureModel:
            if obj.stereotypes != None:
                if obj.level == 0:
                    if obj.name == "Car":
                        g.add_node(obj.nodeId, level=obj.level)
                        if obj.parentNodeId != None:
                            g.add_edge(obj.nodeId, obj.parentNodeId, rel=obj.relationship)
 
                elif obj.level == 1:    
                    if obj.name == "engine" or obj.name == "lamp" or obj.name == "spoiler" or obj.name == "sunRoof" or obj.name == "door" or obj.name == "wheel" or obj.name == "chassis" or obj.name == "maxMass" or obj.name == "maxOutputPower" or obj.name == "maxSpeed" or obj.name == "fitnessValue":
                        g.add_node(obj.nodeId, level=obj.level)
                        if obj.parentNodeId != None:
                            g.add_edge(obj.nodeId, obj.parentNodeId, rel=obj.relationship)
                            
                elif obj.level == 2:    
                    if obj.name == "filamentBurnoutDetector" or obj.name == "autolevelingMotor" or obj.name == "fitness":
                        g.add_node(obj.nodeId, level=obj.level)
                        if obj.parentNodeId != None:
                            g.add_edge(obj.nodeId, obj.parentNodeId, rel=obj.relationship)

                elif obj.level == 3:    
                    if obj.name == "Fitness Value Function":
                        g.add_node(obj.nodeId, level=obj.level)
                        if obj.parentNodeId != None:
                            g.add_edge(obj.nodeId, obj.parentNodeId, rel=obj.relationship)
                            
                elif obj.level == 4:    
                    if obj.name == "fitnessMass" or obj.name == "fitnessSpeed" or obj.name == "fitnessPower":
                        g.add_node(obj.nodeId, level=obj.level)
                        if obj.parentNodeId != None:
                            g.add_edge(obj.nodeId, obj.parentNodeId, rel=obj.relationship)
                            
        pos = nx.nx_pydot.graphviz_layout(g, prog="dot")

        plt.figure(figsize=(20,10))
        nx.draw_networkx_nodes(g, pos, node_size=900, node_color="W")
        nx.draw_networkx_labels(g, pos)
        nx.draw_networkx_edges(g, pos)
        nx.draw_networkx_edge_labels(g, pos, font_color="r")
        plt.axis("off")
        plt.show()