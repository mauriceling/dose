'''!
Exceptions Defined for COPADS. 

    - CopadsError
        - MatrixError
        - GraphError
            - EdgeNotFoundError
            - VertexNotFoundError
            - UnknownGraphMatrixError
                - NotAdjacencyGraphMatrixError
            - GraphEdgeSizeMismatchError
        - StatisticsError
            - DistributionError
                - NormalDistributionTypeError
            - DistributionParameterError
            - DistributionFunctionError
        - DistanceError
            - DistanceInputSizeError
        - TreeError
            - TreeNodeTypeError
        - FunctionParameterTypeError
        - FunctionParameterValueError
        - ParallelArrayError
        - MaxIterationException
        - VectorError

Credits
    - MatrixError subclasses 
    (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189971)

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 1st May 2005
'''

class CopadsError(Exception):
    '''!
    Base class for all Copads-defined exceptions.
    '''
    pass
        

class MatrixError(CopadsError):
    '''!
    Exception to be thrown when encountered errors in Matrix onject.
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg

    
class GraphError(CopadsError):
    '''!
    Abstract parent for all graph exceptions
    '''
    pass

class EdgeNotFoundError(GraphError):
    '''!
    Exception to be thrown when trying to retrieve an edge that is not 
    found in the graph.
    '''
    def __init__(self, edge): self.edge = edge
    def __str__(self): return "Edge, %s, is not found." % self.edge
        
class VertexNotFoundError(GraphError):
    '''!
    Exception to be thrown when trying to retrieve a vertex that is 
    not found in the graph.
    '''
    def __init__(self, vertex): self.vertex = vertex
    def __str__(self): return "Vertex, %s, is not found." % self.vertex
        
class UnknownGraphMatrixError(GraphError):
    '''!
    Exception to be thrown when trying to use an unknown type of graph 
    matrix.
    '''
    def __init__(self, type): self.type = type
    def __str__(self): return "Graph matrix type, %s, is not known." \
        % self.type
        
class NotAdjacencyGraphMatrixError(UnknownGraphMatrixError):
    '''!
    Exception to be thrown when trying to enter a non-square matrix 
    into Graph.GraphAdjacencyMatrix object or when not supplying an 
    adjacency matrix when the calculation requires it.
    '''
    def __init__(self, type): self.type = type
    def __str__(self):
        return 'The graph inputted or required is not an adjacency matrix.'
        
class GraphEdgeSizeMismatchError(GraphError):
    '''!
    Exception for number of output edges do not match the number of 
    input edges.
    '''
    def __init__(self, index, edge):
        self.index = index
        self.edge = edge

    def __str__(self):
        return "Number of edges do not match at index %s, %s" % \
               (str(self.index), str(self.edge))
        
class GraphParameterError(GraphError):
    '''!
    Exception for parameter errors in Graph.Graph class.
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    

class StatisticsError(CopadsError):
    '''
        Abstract parent for all statistics exceptions
    '''
    pass
    
class DistributionError(StatisticsError):
    '''!
        Abstract parent for all exceptions pertaining to statistical
        distributions
    '''
    pass
    
class NormalDistributionTypeError(DistributionError):
    '''!
    Exception for type errors in normal distribution 
    (StatisticsDistribution.NormalDistribution).
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class DistributionParameterError(DistributionError):
    '''!
    Exception for parameter errors in distributions 
    (StatisticsDistribution.*).
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class DistributionFunctionError(DistributionError):
    '''!
    Exception for undefined functions in distributions 
    (StatisticsDistribution.*).
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class DistanceError(CopadsError):
    '''!
    Abstract parent for all exceptions related to calculating 
    distances between lists.
    '''
    pass
    
class DistanceInputSizeError(DistanceError):
    '''!
    Exception for input parameter size errors for list (object) 
    distance routines that have specific requirements for the size of 
    inputs.
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class TreeError(CopadsError):
    '''!
    Abstract parent for all tree exceptions
    '''
    pass

class TreeNodeTypeError(TreeError):
    '''!
    Exception to be thrown when trying to add a non-Node class object 
    (Tree.Node) into a Tree object (Tree.BinaryTree)
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class FunctionParameterTypeError(CopadsError):
    '''!
    Exception to be thrown when trying a function parameter is of the 
    wrong data type
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class FunctionParameterValueError(CopadsError):
    '''!
    Exception to be thrown when trying a function parameter is of 
    wrong value
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class ParallelArrayError(CopadsError):
    '''!
    Exception to be thrown when encountered error in ParallelArray type'''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    
class MaxIterationsException(CopadsError):
    '''!
    Exception to catch maximum looping.
    '''
    pass
    
class VectorError(CopadsError):
    '''!
    Exception to be thrown when encountered errors in Vector onject.
    '''
    def __init__(self, msg): self.msg = msg
    def __str__(self): return self.msg
    