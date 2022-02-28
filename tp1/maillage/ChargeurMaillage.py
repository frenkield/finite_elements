import logging
from typing import TextIO

import numpy

from maillage.MaillageTriangulaire import MaillageTriangulaire

NODES_LINE = "$Noeuds"
ELEMENTS_LINE = "$Elements"


class ChargeurMaillage:

    def advance_to_line(self, file: TextIO, line_text: str) -> bool:
    
        while True:
    
            line = file.readline().strip()
    
            if not line:
                return False
    
            if line == line_text:
                return True
    
    def read_nodes(self, file: TextIO) -> numpy.array:
    
        node_count = int(file.readline().strip())
        logging.debug("node count = %d", node_count)
    
        nodes = numpy.zeros((node_count, 3), dtype=float)
    
        for i in range(node_count):
            node_text = file.readline().strip()

            if not node_text:
                continue
            
            node_data = node_text.split()
            
            index = int(node_data[0])
            x = float(node_data[1])
            y = float(node_data[2])
            z = float(node_data[3])
            
            nodes[index, 0] = x
            nodes[index, 1] = y
            nodes[index, 2] = z
        
        return nodes
    
    
    def read_elements(self, file: TextIO) -> numpy.array:
    
        element_count = int(file.readline().strip())
        logging.debug("element count = %d", element_count)
    
        elements = numpy.zeros((element_count, 3), dtype=int)
    
        for i in range(element_count):
            
            element_text = file.readline().strip()
            
            if not element_text:
                continue
            
            element_data = element_text.split()
            
            index = int(element_data[0])
            node1 = int(element_data[1])
            node2 = int(element_data[2])
            node3 = int(element_data[3])
            
            elements[index, 0] = node1
            elements[index, 1] = node2
            elements[index, 2] = node3
    
        return elements
    
    
    def charger_maillage(self, filename) -> MaillageTriangulaire:
    
        with open(filename) as donneesMaillage:
        
            nodes_line = self.advance_to_line(donneesMaillage, NODES_LINE)
            assert nodes_line, "ligne %s pas trouvée dans %s" % (NODES_LINE, filename)
            nodes = self.read_nodes(donneesMaillage)
        
            elements_line = self.advance_to_line(donneesMaillage, ELEMENTS_LINE)
            assert elements_line, "ligne %s pas trouvée dans %s" % (ELEMENTS_LINE, filename)
            elements = self.read_elements(donneesMaillage)
            
            maillage = MaillageTriangulaire(nodes, elements)
            return maillage
        