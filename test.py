
import sys
import game
import algorithms
import copy
import time


class BackTracking(algorithms.Algorithm):

    def __init__(self) -> None:
        super().__init__()


    def build_constraints2(self, variables):
        vars = list(variables.keys())

        constraints = {var: [] for var in vars}

        for i in range(len(vars)):
            j = i + 1
            var1 = vars[i]
            fields1 = variables[var1]['fields']
            while j < len(vars):
                var2 = vars[j]

                for ind, field in enumerate(variables[var2]['fields']):
                    if field in fields1:
                        constraints[var1].append({'type': 1, 'var': var2, 'var_ind': ind, 'my_ind': fields1.index(field)})
                        constraints[var2].append({'type': 1, 'var': var1, 'var_ind': fields1.index(field), 'my_ind': ind})
                        
                j = j + 1

        return constraints

    def build_constraints3(self, variables, tiles):

        var_fields = {var: [] for var in variables.keys()}
        row_len = len(tiles[0])

        for var in variables.keys():

            var_len = variables[var]
            var_num = int(var[:-1])
            i = var_num // row_len
            j = var_num % row_len

            if var[-1] == 'h':
                var_fields[var] = [(row_len * i  + j + inc) for inc in range(var_len)]
            if var[-1] == 'v':
                var_fields[var] = [((row_len * (i + inc))  + j) for inc in range(var_len)]

        print('VARS')
        for k, v in variables.items():
            print(k, " ", v)

        print('VAR FIELDS')
        for k, v in var_fields.items():
            print(k, " ", v)


        vars = list(variables.keys())
        constraints = {var: {} for var in vars}

        for i in range(len(vars)):
            j = i + 1
            var1 = vars[i]
            fields1 = var_fields[var1]
            while j < len(vars):
                var2 = vars[j]

                for ind, field in enumerate(var_fields[var2]):
                    if field in fields1:
                        constraints[var1][var2] = {'var_ind': ind, 'my_ind': fields1.index(field)}
                        constraints[var2][var1] = {'var_ind': fields1.index(field), 'my_ind': ind}
                        
                j = j + 1

        print('CONSTRAINTS')
        for k, v in constraints.items():
            print(k, " ", v)

        return constraints
    

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

                if len(fields1) == len(variable_fields[var2]):
                    constraints[var1].append({'type': 0, 'var': var2})
                    constraints[var2].append({'type': 0, 'var': var1})

                for ind, field in enumerate(variable_fields[var2]):
                    if field in fields1:
                        constraints[var1].append({'type': 1, 'var': var2, 'var_ind': ind, 'my_ind': fields1.index(field)})
                        constraints[var2].append({'type': 1, 'var': var1, 'var_ind': fields1.index(field), 'my_ind': ind})
                        
                j = j + 1

        return constraints

    def build_domains(self, variables, words):
        domains = {}
        # domain entry
        for var, length in variables.items():
            domains[var] = [word for word in words if len(word) == length]
        
        return domains

    def check_intersection(self, x_val, y_val, constraint):
        #return True if vars have the same letter at intersecting indexes
        x_ind = constraint['my_ind']
        y_ind = constraint['var_ind']
        return x_val[x_ind] == y_val[y_ind]


    def is_consistent(self, sel_var, sel_val, vars, domains, constraints):
        #var - selected variable
        #val - potential variable value
        #domains - other variable domains
        #constraints - variable constraints

        for constraint_var, constraint in constraints[sel_var].items():

            #one word multiple times

            # if constraint['type'] == 0:
            #     #cannot be the same
            #     if domains[constraint['var']]['val'] == sel_val:
            #         print('VAL: ', sel_val, ' already taken VAR: ', constraint['var'])
            #         return False 

            if constraint['type'] == 1:
                #intersecting
                #if they hawe different chars at intersecting fields
                comparing_var_val = vars[constraint_var]
                if comparing_var_val is not None:
                    if not self.check_intersection(sel_val, comparing_var_val, constraint):
                        print('VAL: ', sel_val, ' my_ind: ', constraint['my_ind'], ' and VAL: ', comparing_var_val, ' var_ind: ', constraint['var_ind'],  'in VAR: ', constraint_var, ' dont match')
                        return False
                    # if comparing_var_val[var_ind] != sel_val[my_ind]:
                    #     print('VAL: ', sel_val, ' my_ind: ', my_ind, ' and VAL: ', comparing_var_val, ' var_ind: ', var_ind,  'in VAR: ', constraint['var'], ' dont match')
                    #     return False

        return True

    def backtrack(self, vars, words, curr_var_ind, domains, constraints, solution, var_values):
        if curr_var_ind == len(vars):
            print("END")
            print("---------------------")
            return True

        var = list(vars.keys())[curr_var_ind]

        print("---------------------")
        print("VAR: ", var)

        for ind, val in enumerate(domains[var]):
            print("VAR: ", var)
            if self.is_consistent(var, val, vars, domains, constraints):
                print("     VAL: ", val, " OK")
                solution.append([var, ind, domains])
                copied_domains = copy.deepcopy(domains)
                copied_vars = copy.deepcopy(vars)
                copied_domains[var] = [val]
                copied_vars[var] = val
                var_values[var] = val
                if self.backtrack(copied_vars, words, curr_var_ind+1, copied_domains, constraints, solution, var_values):
                    print("STEP UP")
                    print("---------------------")
                    return True
            else:
                print("     VAL: ", val, " NOT OK")
        
        #backtrack
        solution.append([var, None, domains])
        print("BACKTRACK")
        print("---------------------")
        return False

    def get_algorithm_steps(self, tiles, variables, words):

        #build domains:
        domains = self.build_domains(variables, words)
        print("Domains")
        #print(domains)
        for var, domain in domains.items():
            print(var, " ", domain)

        #build constraints:
        constraints = self.build_constraints3(variables, tiles)
        print("Constraints")

        #print(constraints)

        curr_var_ind = 0
        solution = []
        var_values = {var: None for var in variables.keys()}

        #call backtrack algorithm

        print("Backtrack START")
        success = self.backtrack({var: None for var in variables.keys()}, words, curr_var_ind, domains, constraints, solution, var_values)
        print("Backtrack END")
        if success:
            print("STEPS: ", len(solution))
            print(solution)
            print("SOLUTON")
            print(var_values)
        else:
            print("Solution does not exist")

        #print(domains)


class ForwardChecking(algorithms.Backtracking):

    def forward_check_vars(self, sel_var, sel_val, vars, domains, constraints):
        
        print("FORWARD CHECKING - VAR: ", sel_var, " VAL: ", sel_val)
        for constraint_var, constraint in constraints[sel_var].items():
            
            #constraining variable
            #comparing_var = constraint['var']

            #value not yet assigned
            if vars[constraint_var] is None:
                remove_list = []
                my_ind = constraint['my_ind']
                var_ind = constraint['var_ind']
                for word in domains[constraint_var]:
                    if word[var_ind] != sel_val[my_ind]:
                        remove_list.append(word)

                print("DOMAIN BEFORE FORWARD CHECKING - VAR: ", constraint_var)
                print(domains[constraint_var])

                for word in remove_list:
                    domains[constraint_var].remove(word)
                    print(word, " removed from domain for VAR: ", constraint_var)

                print("DOMAIN AFTER FORWARD CHECKING - VAR: ", constraint_var)
                print(domains[constraint_var])


                if not len(domains[constraint_var]):
                    return False

        return True

            

    def backtrack(self, vars, words, curr_var_ind, domains, constraints, solution, var_values):
        if curr_var_ind == len(vars):
            print("END")
            print("---------------------")
            return True

        var = list(vars.keys())[curr_var_ind]

        print("---------------------")
        print("VAR: ", var)

        for ind, val in enumerate(domains[var]):
            print("VAR: ", var)
            if self.is_consistent(var, val, vars, domains, constraints):
                print("     VAL: ", val, " OK")
                solution.append([var, ind, domains])
                copied_domains = copy.deepcopy(domains)
                copied_vars = copy.deepcopy(vars)
                copied_domains[var] = [val]
                copied_vars[var] = val
                var_values[var] = val
                if not self.forward_check_vars(var, val, copied_vars, copied_domains, constraints):
                    #if var domain is empty after forward cheking do not continue search
                    print("DOMAIN EMPTY")
                    continue
                if self.backtrack(copied_vars, words, curr_var_ind+1, copied_domains, constraints, solution, var_values):
                    print("STEP UP")
                    print("---------------------")
                    return True
            else:
                print("     VAL: ", val, " NOT OK")
        
        #backtrack
        solution.append([var, None, domains])
        print("BACKTRACK")
        print("---------------------")
        return False



class ArcConsistency(algorithms.ForwardChecking):

    def get_arcs(self, constraints):
        arcs = []
        for var, var_constraints in constraints.items():
            for constraint_var, constraint in var_constraints.items():
                arcs.append((var, constraint_var, constraint))

        return arcs

    def get_arcs2(self, variables, constraints):
        arcs = []
        for var, var_constraints in constraints.items():
            if variables[var] is not None:
                #value already assigned
                continue

            for constraint_var, constraint in var_constraints.items():
                if variables[constraint_var] is not None:
                    #value already assigned
                    continue

                arcs.append((var, constraint_var, constraint))

        return arcs

    def resolve_inconsistency(self, sel_var, sel_val, vars, domains, constraints):
        arcs = self.get_arcs2(vars, constraints)
        print("RESOLVING INCONSISTENCIES")
        while len(arcs):
            x, y, constraint = arcs.pop(0)
            print("ARC X: ", x, " Y: ", y)
            if x != sel_var and y != sel_var:
                x_remove = []
                for x_val in domains[x]:
                    remove = True
                    for y_val in domains[y]:
                        if self.check_intersection(x_val, y_val, constraint):
                            remove = False
                            break
                    if remove:
                        x_remove.append(x_val)

                print("DOMAIN BEFORE AC - VAR: ", x)
                print(domains[x])

                if len(x_remove):

                    for word in x_remove:
                        domains[x].remove(word)
                        print(word, " removed from domain for VAR: ", x)
                    
                    if not len(domains[x]):
                        return False
                    
                    for constraint_var, constraint in constraints[x].items():
                        if constraint_var != sel_var and vars[constraint_var] is None:
                            arcs.append((constraint_var, x, constraints[constraint_var][x]))
                            print("ARC X: ", constraint_var, " Y: ", x, " ADDED")

                print("DOMAIN AFTER AC - VAR: ", x)
                print(domains[x])

        return True

    def backtrack(self, vars, words, curr_var_ind, domains, constraints, solution, var_values):
        if curr_var_ind == len(vars):
            print("END")
            print("---------------------")
            return True

        var = list(vars.keys())[curr_var_ind]

        print("---------------------")
        print("VAR: ", var)

        for ind, val in enumerate(domains[var]):
            print("VAR: ", var)
            if self.is_consistent(var, val, vars, domains, constraints):
                print("     VAL: ", val, " OK")
                solution.append([var, ind, domains])
                copied_domains = copy.deepcopy(domains)
                copied_vars = copy.deepcopy(vars)
                copied_domains[var] = [val]
                copied_vars[var] = val
                var_values[var] = val
                if not self.forward_check_vars(var, val, copied_vars, copied_domains, constraints):
                    #if var domain is empty after forward cheking do not continue search
                    print("DOMAIN EMPTY")
                    continue
                if not self.resolve_inconsistency(var, val, vars, copied_domains, constraints):
                    #if var domain is empty after forward cheking do not continue search
                    print("DOMAIN EMPTY")
                    continue
                if self.backtrack(copied_vars, words, curr_var_ind+1, copied_domains, constraints, solution, var_values):
                    print("STEP UP")
                    print("---------------------")
                    return True
            else:
                print("     VAL: ", val, " NOT OK")
        
        #backtrack
        solution.append([var, None, domains])
        print("BACKTRACK")
        print("---------------------")
        return False

    def test(self, tiles, variables, words):
        #build domains:
        domains = self.build_domains(variables, words)
        print("Domains")
        #print(domains)
        for var, domain in domains.items():
            print(var, " ", domain)

        #build constraints:
        constraints = self.build_constraints(variables, tiles)
        print("Constraints")
        print(constraints)

        arcs = self.get_arcs(constraints)
        print("Arcs")
        print(arcs)

        curr_var_ind = 0
        solution = []
        var_values = {var: None for var in variables.keys()}

        #call backtrack algorithm

        # print("Backtrack START")
        # success = self.backtrack({var: None for var in variables.keys()}, words, curr_var_ind, domains, constraints, solution, var_values)
        # print("Backtrack END")
        # if success:
        #     print("STEPS: ", len(solution))
        #     print(solution)
        #     print("SOLUTON")
        #     print(var_values)
        # else:
        #     print("Solution does not exist")

        #print(domains)



if __name__ == "__main__":
    shcema_file = sys.argv[1]
    words_file = sys.argv[2]
    alg = int(sys.argv[3])

    tiles = game.Game.load_schema(shcema_file)
    words = game.Game.load_words(words_file)
    variables = game.Game.get_variables(tiles)

    print(variables)
    start_t = time.time()
    if alg == 0:
        BackTracking().build_constraints3(variables, tiles)
    elif alg == 1:
        print("Backtracking")
        BackTracking().get_algorithm_steps(tiles, variables, words)
    elif alg == 2:
        print("Backtracking + ForwardChecking")
        ForwardChecking().get_algorithm_steps(tiles, variables, words)
    elif alg == 3:
        print("Get all arcs test")
        ArcConsistency().test(tiles, variables, words)
    elif alg == 4:
        print("Get all arcs test")
        ArcConsistency().get_algorithm_steps(tiles, variables, words)
    print("Elapsed time: ", time.time() - start_t)
    
    # print(tiles)
    # print(words)
    # print(variables)

    