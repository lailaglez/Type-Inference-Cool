import cmp.visitor as visitor
from AST.AST_Hierarchy import *
from cmp.semantic import SemanticError
from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, ErrorType
from cmp.semantic import Context

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for dec in node.declarations:
            self.visit(dec)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.id)
            if node.parent is not None:
                try:
                    typex = self.context.get_type(node.parent)
                except SemanticError as error:
                    self.errors.append(error.text)
                    typex = ErrorType()
                self.current_type.set_parent(typex)
        except SemanticError as error:
            self.errors.append(error.text)
            
        for feature in node.features:
                self.visit(feature)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            typex = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(error.text)
            typex = ErrorType()
            
        try:
            self.current_type.define_attribute(node.id, typex)
        except SemanticError as error:
            self.errors.append(error.text)
        
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        param_names = []    
        param_types = []
        for param in node.params:
            param_names.append(param[0])
            try:
                typex = self.context.get_type(param[1])
            except SemanticError as error:
                self.errors.append(error.text)
                typex = ErrorType()
            param_types.append(typex)

        try:
            typex = self.context.get_type(node.type)
        except SemanticError as error:
            self.errors.append(error.text)
            typex = ErrorType()
        
        try:
            self.current_type.define_method(node.id, param_names, param_types, typex)
        except SemanticError as error:
            self.errors.append(error.text)
        
