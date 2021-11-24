# ====================
# 사람과 AI의 대전
# ====================

# 패키지 임포트
from game import State
from pv_mcts import pv_mcts_action, pv_mcts_scores
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

# 베스트 플레이어 모델 로드
model = load_model("./model/best.h5")

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
CELL_SIZE = int(CANVAS_WIDTH / 6)

# 게임 UI 정의
class GameUI(tk.Frame):
    # 초기화
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title("오셀로")

        # 게임 상태 생성
        self.state = State()

        # PV MCTS를 활용한 행동을 선택하는 함수 생성
        self.next_action = pv_mcts_action(model, 0.0)

        # 캔버스 생성
        self.c = tk.Canvas(
            self, width=CANVAS_WIDTH, height=CANVAS_WIDTH, highlightthickness=0
        )
        self.c.bind("<Button-1>", self.turn_of_human)
        self.c.pack()

        # 화면 갱신
        self.on_draw()

    # 사람의 턴
    def turn_of_human(self, event):
        # 게임 종료 시
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 선 수가 아닌 경우
        if not self.state.is_first_player():
            return

        # 클릭 위치를 행동으로 변환
        x = int(event.x / CELL_SIZE)
        y = int(event.y / CELL_SIZE)
        print(x, y)
        if x < 0 or 5 < x or y < 0 or 5 < y:  # 범위 외
            return
        action = x + y * 6

        # 합법적인 수가 아닌 경우
        legal_actions = self.state.legal_actions()
        if legal_actions == [36]:
            action = 36  # 패스
        if action != 36 and not (action in legal_actions):
            return

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

        # AI의 턴
        self.master.after(1, self.turn_of_ai)

    # AI의 턴
    def turn_of_ai(self):
        # 게임 종료 시
        if self.state.is_done():
            return

        # 행동 얻기
        action = self.next_action(self.state)

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

    # 돌 그리기
    def draw_piece(self, index, first_player):
        x = (index % 6) * CELL_SIZE + int(CELL_SIZE / 10)
        y = int(index / 6) * CELL_SIZE + int(CELL_SIZE / 10)
        if first_player:
            self.c.create_oval(
                x,
                y,
                x + int(CELL_SIZE / 5) * 4,
                y + int(CELL_SIZE / 5) * 4,
                width=1.0,
                outline="#000000",
                fill="#404040",
            )
        else:
            self.c.create_oval(
                x,
                y,
                x + int(CELL_SIZE / 5) * 4,
                y + int(CELL_SIZE / 5) * 4,
                width=1.0,
                outline="#000000",
                fill="#FFFFFF",
            )

    def draw_legal_actions(self, legal_actions, scores):
        for action, score in zip(legal_actions, scores):
            x = (action % 6) * CELL_SIZE + int(CELL_SIZE / 3)
            y = int(action / 6) * CELL_SIZE + int(CELL_SIZE / 3)
            self.c.create_oval(
                x,
                y,
                x + int(CELL_SIZE / 3),
                y + int(CELL_SIZE / 3),
                width=1.0,
                outline="#000000",
                fill="#FF0000",
            )

            # draw text of score on the cell
            self.c.create_text(
                x + int(CELL_SIZE / 3),
                y + int(CELL_SIZE / 3),
                text=round(score * 100, 3),
                fill="#000000",
                font=("Arial", 12, "bold"),
            )

    # 화면 갱신
    def on_draw(self):
        self.c.delete("all")
        self.c.create_rectangle(
            0, 0, CANVAS_WIDTH, CANVAS_WIDTH, width=0.0, fill="#54956B"
        )
        for i in range(1, 8):
            self.c.create_line(
                0, i * CELL_SIZE, CANVAS_WIDTH, i * CELL_SIZE, width=2.0, fill="#404040"
            )
            self.c.create_line(
                i * CELL_SIZE, 0, i * CELL_SIZE, CANVAS_WIDTH, width=2.0, fill="#404040"
            )

        is_first_player = self.state.is_first_player()
        for i in range(36):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, is_first_player)
            elif self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not is_first_player)

        if is_first_player:
            # 합법적인 수의 확률 분포 얻기
            scores = pv_mcts_scores(model, self.state, 1.0)
            legal_actions = self.state.legal_actions()
            print(f"{scores=}")
            print(f"{legal_actions=}")
            self.draw_legal_actions(legal_actions, scores)
            print("플레이어 턴")


# 게임 UI 실행
f = GameUI(model=model)
f.pack()
f.mainloop()
