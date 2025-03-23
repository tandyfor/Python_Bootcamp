from src.web.mapper import WebMapper
from src.web.module import WebSession
from src.di.container import Container
from src.domain.model import NOUGHT, CROSS

from flask import Flask, request, jsonify, redirect, url_for


app = Flask(__name__)
container = Container()

@app.route('/game/', methods=['GET'])
def start():
    session = WebSession(container)
    session.save()
    return redirect(url_for('play', uuid=session.domain_service.model.uuid))

@app.route('/game/<uuid:uuid>', methods=['GET', 'POST'])
def play(uuid):
    session = WebSession(container)
    session.domain_service.model = session.container.get(uuid)

    if request.method == 'GET':
        return jsonify(WebMapper.domain_model_2_json(session.domain_service.model))

    if request.method == 'POST':
        try:
            model = WebMapper.json_2_web_model(request.get_json())
            model = WebMapper.web_model_2_domin_model(model)

            if not session.domain_service.validate(model):
                return jsonify({"error": "Invalid move"}), 400

            session.domain_service.model = model

            if session.domain_service.game_over():
                winner = session.domain_service.check_winner()
                if winner == CROSS:
                    session.save()
                    return jsonify({"message": "User wins!"}), 200
                return jsonify({"message": "It's a draw!"}), 200

            session.domain_service.computer_move()

            if session.domain_service.game_over():
                winner = session.domain_service.check_winner()
                if winner == NOUGHT:
                    session.save()
                    return jsonify({"message": "Computer wins!"}), 200
                return jsonify({"message": "It's a draw!"}), 200

            container.save(session.domain_service)
            return jsonify(WebMapper.domain_model_2_json(session.domain_service.model))
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/games/', methods=['GET'])
def get_games():
    return container.storage.storage


if __name__ == '__main__':
    app.run(debug=True)