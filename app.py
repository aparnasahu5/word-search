from flask import Flask, render_template, request, redirect, url_for
from typing import List, Tuple
from itertools import product
import random
from collections import Counter

app = Flask(__name__)

def generate_random_grid():
    alphabets = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    grid = [[random.choice(alphabets) for _ in range(9)] for _ in range(9)]
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
        result = sol.exist(random_grid, user_input)
        return render_template('index.html', grid=random_grid, result=result)
    else:
        return render_template('index.html', grid=random_grid, result=None)

@app.route('/generate_grid', methods=['POST'])
def generate_grid():
    random_grid = generate_random_grid()
    return redirect(url_for('index'))

if __name__ == '__main__':
    random_grid = generate_random_grid()
    app.run(debug=True)
