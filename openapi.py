from flask import Flask, jsonify, request
import flask
import json
from textwrap import dedent # 들여쓰기 패키지
from uuid import uuid4 # 고유한 난수 발생하는 패키지
import sys
from Blockchain import Blockchain # Blockchain 클래스에서 Blockchain 모듈


app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')
blockchain = Blockchain()


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    """
    {"node" : ["http://127.0.0.1:5000"]}
    """
    nodes = values.get("nodes")
    if nodes is None:
        return "Error: please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        "message": "new nodes have been added.",
        "total_nodes": list(blockchain.nodes),
    }

    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    is_newchain = blockchain.resolve_conflicts()

    if is_newchain:
        response = {
            "message" : "Out chain was replaced",
            "new_chain": blockchain.chain
        }

    else:
        response = {
            "message" : "Out chain is authoritative",
            "chain": blockchain.chain
        }
    
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof) # 9675
    
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )    

    previous_hash = blockchain.hash(last_block) # ABCDE
    created_block = blockchain.new_block(proof, previous_hash)

    response = {
        "message": "New Block created.",
        "index": created_block['index'],
        "transaction": created_block['transactions'],
        "proof": created_block['proof'],
        "previous_hash": created_block['previous_hash']

    }

    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return "Missing values", 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {"message": f"Transaction will be added to Block {index}"}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def retrieve_chain():
    response = {
        'blockchain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/list', methods=['GET'])
def retrieve_all_nodes():
    courrent_list = list(blockchain.nodes)
    """
    current_list의 노드들의 검증 -> /check 호출
    """
    response = {
        "message":"Total nodes list",
        "total_nodes": "courrent_list"

    }

    return jsonify(response), 201

@app.route('/check', methods=['GET'])
def node_check():
    response = {
        'result':'OK',
    }

    return jsonify(response), 200

@app.route('/getinfo/<path:blockid>', methods=['GET'])
def retrieve_node_info(blockid):
    # blockchain.chain[int(blockid) - 1]
    response = {
        "message" : f"Block[{blockid}]'s information",
    }

    return jsonify(response), 200

if __name__ == '__main__':
    print("Node="+ node_identifier)
    # app.run(host='0.0.0.0', port=sys.argv[1])
    app.run(host='0.0.0.0', port=5001)
    
    