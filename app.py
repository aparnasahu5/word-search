from flask import Flask, render_template, request, redirect, url_for, session
from typing import List, Tuple
from itertools import product
import random
from collections import Counter

app = Flask(__name__)
app.secret_key = 'super_secret_key'

def generate_random_grid(previous_grid=None):
    alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    
    while True:
        grid = [[random.choice(alphabets) for _ in range(9)] for _ in range(9)]
        if grid != previous_grid:
            return grid

class Solution:
    def exist(self, board: List[List[str]], word: str) -> List[Tuple[int, int]]:
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        m, n = len(board), len(board[0])

        def is_valid(x, y):
            return 0 <= x < m and 0 <= y < n

        def backtrack(i, j, k, visited):
            if board[i][j] == word[k]:
                if k == len(word) - 1:
                    return [(i, j)]
                result = []
                for xn, yn in directions:
                    x, y = i + xn, j + yn
                    if is_valid(x, y) and (x, y) not in visited:
                        new_visited = visited.union({(x, y)})
                        sub_result = backtrack(x, y, k + 1, new_visited)
                        if sub_result:
                            result.extend([(i, j)] + sub_result)
                return result
            return []

        for i, j in product(range(m), range(n)):
            result = backtrack(i, j, 0, {(i, j)})
            if result:
                return result

        return []
        # ... (the rest of your Solution class code)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['word'].upper()
        sol = Solution()
        result = sol.exist(session['random_grid'], user_input)
        return render_template('index.html', grid=session['random_grid'], result=result)
    else:
        session['random_grid'] = generate_random_grid()
        return render_template('index.html', grid=session['random_grid'], result=None)

@app.route('/generate_grid', methods=['POST'])
def generate_grid():
    session['random_grid'] = generate_random_grid(session['random_grid'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    random_grid = generate_random_grid()
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
