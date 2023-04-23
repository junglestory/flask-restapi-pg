from flask import Flask, jsonify, request
from models import db
from models import Board
from db.database import SQLALCHEMY_DATABASE_URL

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
db.app = app

@app.route('/hello', methods=['GET'])
def helloworld():
    print("hello")
    return jsonify({"Hello": "World"})


@app.route('/board', methods=['POST'])
def create_board():
    try:
        param = request.get_json()

        if param != None:
            board = Board(param['title'], param['contents'], param['writer'], param['view_count'], param['link_url'])

            db.session.add(board)
            db.session.flush()

            db.session.refresh(board, attribute_names=['board_no'])
            data = {"board_no": board.board_no}

            db.session.commit()

            status = True
            message = "Board added successfully."
    except Exception as e:
        status = False
        data = None
        message = e

    result_data = {"status": "{}".format(status), "message": "{}".format(message), "data": data}

    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)