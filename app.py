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


@app.route('/board', defaults={'board_no': ''}, methods=['GET'])
@app.route('/board/<board_no>', methods=['GET'])
def board(board_no):
    results = []
    datas = []

    if board_no != "":
        datas = Board.query.filter_by(board_no = board_no).all()
    else:
        datas = Board.query.all()

    for data in datas:
        results.append(data.to_json())

    return jsonify(results)


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


@app.route('/board', methods=['PUT'])
def update_board():
    try:
        status = True
        message = "Board updated successfully"

        param = request.get_json()

        result = db.session.query(Board).filter(Board.board_no == param['board_no']).update({
            'title': param['title'],
            'contents': param['contents'],
            'writer': param['writer'],
            'view_count': param['view_count'],
            'link_url': param['link_url']
        })

        db.session.flush()
        db.session.commit()

        if result == 1:
            data = db.session.query(Board).filter(Board.board_no == param['board_no']).one()
        elif result == 0:
            message = "Board not updated. No product found with this board_no :" + \
                str(param['board_no'])
            status = False
            data = None
    except Exception as e:
        status = False
        data = None
        message = e

    result_data = {"status": "{}".format(status), "message": "{}".format(message), "data": data.to_json()}

    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)