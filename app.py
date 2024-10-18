from flask import Flask, request, jsonify
from models import db
from config import Config
from rule_engine import create_rule, combine_rules, evaluate_rule, add_rule_to_db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule_string')
    rule_ast = create_rule(rule_string)
    return jsonify({"ast": str(rule_ast)})

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rules = request.json.get('rules')
    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": str(combined_ast)})

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    rule_ast = request.json.get('rule_ast')
    data = request.json.get('data')
    result = evaluate_rule(rule_ast, data)
    return jsonify({"result": result})

@app.route('/add_rule', methods=['POST'])
def add_rule():
    rule_string = request.json.get('rule_string')
    add_rule_to_db(rule_string)
    return jsonify({"message": "Rule added to database."})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
