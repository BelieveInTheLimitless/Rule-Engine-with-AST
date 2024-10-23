from ast_structure import Node

def tokenize(rule_string):
    tokens = []
    current = []
    in_quotes = False
    i = 0
    
    while i < len(rule_string):
        char = rule_string[i]
        
        if char == "'":
            if in_quotes and i + 1 < len(rule_string) and rule_string[i + 1] == "'":
                current.append("'")
                i += 1
            else:
                in_quotes = not in_quotes
                current.append(char)
        elif not in_quotes:
            if char in '()':
                if current:
                    tokens.append(''.join(current).strip())
                    current = []
                tokens.append(char)
            elif char.isspace():
                if current:
                    tokens.append(''.join(current).strip())
                    current = []
            elif char in ['>', '<', '=', '!']:
                if current:
                    tokens.append(''.join(current).strip())
                    current = []
                
                if i + 1 < len(rule_string) and rule_string[i:i+2] in ['>=', '<=', '!=']:
                    tokens.append(rule_string[i:i+2])
                    i += 1
                else:
                    tokens.append(char)
            else:
                current.append(char)
        else:
            current.append(char)
        
        i += 1
    
    if current:
        tokens.append(''.join(current).strip())
    
    return [t for t in tokens if t]

def parse_expression(tokens, pos=0):
    stack = []
    operators = []
    
    def apply_operator():
        if len(stack) < 2:
            return
        right = stack.pop()
        left = stack.pop()
        op = operators.pop()
        stack.append(Node("operator", value=op, left=left, right=right))

    while pos < len(tokens):
        token = tokens[pos]
        
        if token == '(':
            subexpr, new_pos = parse_expression(tokens, pos + 1)
            if subexpr:
                stack.append(subexpr)
            pos = new_pos
        elif token == ')':
            while operators:
                apply_operator()
            return stack[0] if stack else None, pos
        elif token.upper() in ['AND', 'OR']:
            while operators and operators[-1] in ['AND', 'OR']:
                if (operators[-1] == 'AND') or (operators[-1] == 'OR' and token.upper() == 'AND'):
                    apply_operator()
                else:
                    break
            operators.append(token.upper())
        else:
            if pos + 2 < len(tokens):
                op = tokens[pos + 1]
                value = tokens[pos + 2]
                if op in ['>', '<', '>=', '<=', '=', '!=']:
                    condition = f"{token} {op} {value}"
                    stack.append(Node("operand", value=condition))
                    pos += 2
                else:
                    stack.append(Node("operand", value=token))
            else:
                stack.append(Node("operand", value=token))
        
        pos += 1
    
    while operators and len(stack) >= 2:
        apply_operator()
    
    return stack[0] if stack else None, pos + 1

def create_rule(rule_string):    
    try:
        rule_string = ' '.join(rule_string.split())
        tokens = tokenize(rule_string)
        
        ast, _ = parse_expression(tokens)
        
        return ast
    except Exception as e:
        print(f"Error parsing rule: {str(e)}")
        return None

def evaluate_rule(rule_ast, data):
    if not rule_ast:
        return False
    
    if rule_ast.type == "operand":
        try:
            field, op, value = rule_ast.value.split()
            
            if value.startswith(("'", '"')) and value.endswith(("'", '"')):
                value = value[1:-1] 
            elif value.replace('.', '').isdigit():
                value = float(value)
            
            if field not in data:
                return False
                
            actual_value = data[field]
            
            if isinstance(value, (int, float)):
                try:
                    actual_value = float(actual_value)
                except (ValueError, TypeError):
                    return False
            
            if op == '>': return actual_value > value
            if op == '<': return actual_value < value
            if op == '>=': return actual_value >= value
            if op == '<=': return actual_value <= value
            if op == '=': return actual_value == value
            if op == '!=': return actual_value != value
            
        except (ValueError, KeyError) as e:
            print(f"Error evaluating condition: {str(e)}")
            return False
    
    if rule_ast.type == "operator":
        left_result = evaluate_rule(rule_ast.left, data)
        right_result = evaluate_rule(rule_ast.right, data)
        
        if rule_ast.value == "AND":
            return left_result and right_result
        elif rule_ast.value == "OR":
            return left_result or right_result
            
    return False