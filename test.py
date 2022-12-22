
import sys
import game
import algorithms


def backtrack():
    pass

class BackTracking(algorithms.Algorithm):

    def __init__(self) -> None:
        super().__init__()
    

    def build_constraints(self, tiles):
        try:
            variable_fields = {}
            for i in range(len(tiles)):
                for j in range(len(tiles[i])):
                    if tiles[i][j]:
                        continue
                    if not j or tiles[i][j - 1]:
                        try:
                            pos = tiles[i][j:].index(True)
                        except ValueError:
                            pos = len(tiles[i]) - j
                        variable_fields[f'{i * len(tiles[i]) + j}h'] = [(len(tiles[i]) * i + j + inc) for inc in range(pos)]
                    if not i or tiles[i - 1][j]:
                        column = [row[j] for row in tiles]
                        try:
                            pos = column[i:].index(True)
                        except ValueError:
                            pos = len(column) - i
                        variable_fields[f'{i * len(tiles[i]) + j}v'] = [((len(tiles[i]) * (i + inc)) + j) for inc in range(pos)]
        except Exception as e:
            raise e
        
        vars = list(variable_fields.keys())

        constraints = {var: [] for var in vars}

        for i in range(len(vars)):
            j = i + 1
            var1 = vars[i]
            fields1 = variable_fields[var1]
            while j < len(vars):
                var2 = vars[j]

                for ind, field in enumerate(variable_fields[var2]):
                    if field in fields1:
                        constraints[var1].append({'var': var2, 'var_index': ind, 'my_ind': fields1.index(field)})
                        constraints[var2].append({'var': var1, 'var_index': fields1.index(field), 'my_ind': ind})
                        
                j = j + 1

        return constraints

    def is_consistent(self):
        return True

    def backtrack(self, vars, lvl, domains, solution):
        if lvl == len(vars):
            return True

        var = vars[lvl]

        for val in domains[var]:
            if self.is_consistent():
                solution.append([var, val[0], domains])

        
        #backtrack
        solution.append([var, None, domains])
        return False

    def get_algorithm_steps(self, tiles, variables, words):

        print(variables)
        ret = self.build_constraints(tiles)
        print(ret)
        #
        domains = {}
        # domain entry
        # var : [(ind, word)...]
        for var, length in variables.items():
            domains[var] = [(ind, word) for ind, word in enumerate(words) if len(word) == length]

        lvl = 0
        solution = []

        #build constraints dir

        self.backtrack(list(variables.keys()), lvl, domains, solution)

        #print(solution)

        #print(domains)






if __name__ == "__main__":
    shcema_file = sys.argv[1]
    words_file = sys.argv[2]
    alg = int(sys.argv[3])

    tiles = game.Game.load_schema(shcema_file)
    words = game.Game.load_words(words_file)
    variables = game.Game.get_variables(tiles)

    if alg == 1:
        print("Backtracking")
        BackTracking().get_algorithm_steps(tiles, variables, words)

    # print(tiles)
    # print(words)
    # print(variables)

    