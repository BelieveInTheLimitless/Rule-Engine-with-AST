import re
from ast_structure import Node
from sqlalchemy.exc import IntegrityError
from models import Rule, db

def create_rule(rule_string):
    rule_string = rule_string.replace('(', ' ( ').replace(')', ' ) ')
    tokens = rule_string.split()
    
    def parse_expression(tokens):
        token = tokens.pop(0)
        if token == '(':
            left = parse_expression(tokens)
            operator = tokens.pop(0)
            right = parse_expression(tokens)
            tokens.pop(0) 
            return Node("operator", left, right, operator)
        else:
            match = re.match(r'(\w+)\s*(>=|<=|>|<|=|!=)\s*(\d+|\'\w+\')', token)
            if match:
                field, op, value = match.groups()
                return Node("operand", value=field + " " + op + " " + value)
            return None
    
    return parse_expression(tokens)

def combine_rules(rules):
    combined_ast = Node("operator") 
    combined_ast.left = create_rule(rules[0])
    for rule in rules[1:]:
        right_node = create_rule(rule)
        combined_ast.right = right_node
    return combined_ast

def evaluate_rule(rule_ast, data):
    if rule_ast.type == "operand":
        field, op, value = rule_ast.value.split()
        value = int(value.strip("'")) if value.isdigit() else value.strip("'")
        if field not in data:
            return False
        return eval(f"{data[field]} {op} {value}")
    
    if rule_ast.type == "operator":
        left_result = evaluate_rule(rule_ast.left, data)
        right_result = evaluate_rule(rule_ast.right, data)
        if rule_ast.value == "AND":
            return left_result and right_result
        elif rule_ast.value == "OR":
            return left_result or right_result
    return False

def add_rule_to_db(rule_string):
    new_rule = Rule(rule_string=rule_string)
    try:
        db.session.add(new_rule)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("Error adding rule to database.")
