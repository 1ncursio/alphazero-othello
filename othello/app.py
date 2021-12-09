from flask import Flask, request

# import flask_cors CORS, cross_origin
from flask_cors import CORS
from tensorflow.keras.models import load_model
from pv_mcts import pv_mcts_action
from game import State

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

model = load_model("./model/best.h5")
next_action = pv_mcts_action(model, 0.0)


@app.route("/")
def hello_world():
    return "test"


@app.route("/api/next_action", methods=["POST"])
def post_request():
    try:
        params = request.get_json()
        pieces = params["pieces"]
        enemy_pieces = params["enemyPieces"]
        depth = params["depth"] if "depth" in params else 0

        state = State(pieces, enemy_pieces, depth)
        # 행동 얻기
        action = int(next_action(state))

        # 다음 상태 얻기
        state = state.next(action)
        if state.is_done():
            # 게임 종료 후 DB에 저장
            "game over"

        print("action", action)

        return {
            "success": True,
            "payload": {
                "action": action,
                "depth": state.depth,
                "pieces": state.pieces,
                "enemyPieces": state.enemy_pieces,
                "isDone": state.is_done(),
                "isDraw": state.is_draw(),
                "isLoss": state.is_loss(),
                # "piecesCount": state.pieces_count(),
            },
            "message": "next action is calculated successfully.",
        }
    except Exception as e:
        return {
            "success": False,
            "payload": {},
            "message": str(e),
        }


if __name__ == "__main__":
    # with credential
    app.run(debug=True)
