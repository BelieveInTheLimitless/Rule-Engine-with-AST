from flask import Flask, request, jsonify, render_template
from models import db, Rule
from config import Config
from rule_engine import create_rule, evaluate_rule, format_ast
from sqlalchemy.exc import OperationalError
import time

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def init_db():
    retries = 5
    while retries > 0:
        try:
            with app.app_context():
                db.create_all()
            print("Database initialized successfully")
            return
        except OperationalError as e:
            retries -= 1
            print(f"Database connection failed. Retrying... ({retries} attempts left)")
            print(f"Error: {e}")
            time.sleep(2)
    
    print("Failed to initialize database after multiple attempts")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_rules', methods=['GET'])
def get_rules():
    try:
        rules = Rule.query.all()
        return jsonify({
            'success': True,
            'rules': [rule.to_dict() for rule in rules]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    try:
        data = request.json
        if not data or 'name' not in data or 'rule_string' not in data:
            return jsonify({
                'success': False,
                'error': 'Both name and rule_string are required'
            }), 400

        name = data['name'].strip()
        rule_string = data['rule_string'].strip()

        if not name or not rule_string:
            return jsonify({
                'success': False,
                'error': 'Name and rule_string cannot be empty'
            }), 400

        existing_rule = Rule.query.filter_by(name=name).first()
        if existing_rule:
            return jsonify({
                'success': False,
                'error': f'Rule with name "{name}" already exists'
            }), 409

        rule_ast = create_rule(rule_string)
        if rule_ast is None:
            return jsonify({
                'success': False,
                'error': 'Invalid rule format'
            }), 400

        formatted_ast = format_ast(rule_ast)

        new_rule = Rule(
            name=name,
            rule_string=rule_string
        )
        
        db.session.add(new_rule)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Rule created successfully',
            'rule': new_rule.to_dict(),
            'ast': formatted_ast
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    try:
        data = request.json
        if not data or 'rules' not in data or 'combined_rule_name' not in data or 'operator' not in data:
            return jsonify({
                "success": False,
                "error": "combined_rule_name, operator, and rules are required"
            }), 400

        combined_rule_name = data['combined_rule_name'].strip()
        operator = data['operator'].strip().upper()
        rules = data['rules']

        if not combined_rule_name or operator not in ['AND', 'OR'] or len(rules) < 2:
            return jsonify({
                "success": False,
                "error": "Invalid input parameters"
            }), 400

        rule_strings = []
        for rule_name in rules:
            rule = Rule.query.filter_by(name=rule_name).first()
            if not rule:
                return jsonify({
                    "success": False,
                    "error": f"Rule not found: {rule_name}"
                }), 404
            rule_strings.append(f"({rule.rule_string})")

        combined_string = f" {operator} ".join(rule_strings)
        combined_ast = create_rule(combined_string)
        
        if combined_ast is None:
            return jsonify({
                "success": False,
                "error": "Failed to create valid combined rule"
            }), 400

        formatted_ast = format_ast(combined_ast)

        new_rule = Rule(
            name=combined_rule_name,
            rule_string=combined_string
        )
        
        db.session.add(new_rule)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Combined rule created successfully",
            "rule": new_rule.to_dict(),
            "ast": formatted_ast
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    try:
        data = request.json
        if not data or 'rule_name' not in data or 'data' not in data:
            return jsonify({
                'success': False,
                'error': 'Both rule_name and data are required'
            }), 400
            
        rule_name = data['rule_name']
        eval_data = data['data']
        
        rule = Rule.query.filter_by(name=rule_name).first()
        if rule is None:
            return jsonify({
                'success': False,
                'error': f'No rule found with name: {rule_name}'
            }), 404
        
        rule_ast = create_rule(rule.rule_string)
        if rule_ast is None:
            return jsonify({
                'success': False,
                'error': 'Invalid rule format'
            }), 400
            
        result = evaluate_rule(rule_ast, eval_data)
        
        return jsonify({
            'success': True,
            'result': result,
            'rule_name': rule_name,
            'rule_string': rule.rule_string,
            'data': eval_data,
            'ast': format_ast(rule_ast)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)