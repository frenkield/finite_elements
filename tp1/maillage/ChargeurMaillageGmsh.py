import logging
from typing import TextIO

import numpy

from maillage.MaillageTriangulaire import MaillageTriangulaire

NODES_LINE = "$Nodes"
ELEMENTS_LINE = "$Elements"


class ChargeurMaillageGmsh:

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
            
            index = int(node_data[0]) - 1
            nodes[index, 0] = float(node_data[1])
            nodes[index, 1] = float(node_data[2])
            nodes[index, 2] = float(node_data[3])
        
        return nodes

    def read_elements(self, file: TextIO) -> numpy.array:
    
        element_count = int(file.readline().strip())
        logging.debug("total element count = %d", element_count)
    
        elements = []
        aretes = []
    
        for i in range(element_count):
            
            element_text = file.readline().strip()
            
            if not element_text:
                continue
            
            element_data = element_text.split()

            # 13 2 2 0 1 7 4 11
            type = int(element_data[1])

            if type == 1:
                node1 = int(element_data[5]) - 1
                node2 = int(element_data[6]) - 1
                aretes.append([node1, node2])

            elif type == 2:
                node1 = int(element_data[5]) - 1
                node2 = int(element_data[6]) - 1
                node3 = int(element_data[7]) - 1
                elements.append([node1, node2, node3])
    
        return numpy.array(elements, dtype=int), numpy.array(aretes, dtype=int)
    
    def charger_maillage(self, filename) -> MaillageTriangulaire:
    
        with open(filename) as donneesMaillage:
        
            nodes_line = self.advance_to_line(donneesMaillage, NODES_LINE)
            assert nodes_line, "ligne %s pas trouvée dans %s" % (NODES_LINE, filename)
            nodes = self.read_nodes(donneesMaillage)
        
            elements_line = self.advance_to_line(donneesMaillage, ELEMENTS_LINE)
            assert elements_line, "ligne %s pas trouvée dans %s" % (ELEMENTS_LINE, filename)
            elements, aretes = self.read_elements(donneesMaillage)
            
            maillage = MaillageTriangulaire(nodes, elements)
            maillage.aretes_du_bord = aretes
            return maillage
