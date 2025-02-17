import sys
import game
import algorithms
import copy
import itertools


class BackTracking(algorithms.Algorithm):

    def __init__(self) -> None:
        super().__init__()

    def build_constraints(self, variables, tiles):

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

    def build_domains(self, variables, words):
        domains = {}
        # domain entry
        for var, length in variables.items():
            domains[var] = [word for word in words if len(word) == length]
        
        return domains


    def is_consistent(self, sel_var, sel_val, vars, domains, constraints):
        #var - selected variable
        #val - potential variable value
        #domains - other variable domains
        #constraints - variable constraints

        for constraint_var, constraint in constraints[sel_var].items():

            #intersecting
            #if they hawe different chars at intersecting fields
            comparing_var_val = vars[constraint_var]
            if comparing_var_val is not None:
                my_ind = constraint['my_ind']
                var_ind = constraint['var_ind']
                if comparing_var_val[var_ind] != sel_val[my_ind]:
                    print('VAL: ', sel_val, ' my_ind: ', my_ind, ' and VAL: ', comparing_var_val, ' var_ind: ', var_ind,  'in VAR: ', constraint_var, ' dont match')
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
        constraints = self.build_constraints(variables, tiles)
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

class ForwardChecking(BackTracking):

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

                print("DOMAIN BEFORE FORWARD CHECKING - VAR: ", constraint_var)
                print(domains[constraint_var])

                for word in domains[constraint_var]:
                    if word[var_ind] != sel_val[my_ind]:
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


if __name__ == "__main__":
    shcema_file = sys.argv[1]
    words_file = sys.argv[2]
    alg = int(sys.argv[3])

    tiles = game.Game.load_schema(shcema_file)
    words = game.Game.load_words(words_file)
    variables = game.Game.get_variables(tiles)

    print(variables)
    if alg == 0:
        BackTracking().build_constraints3(variables, tiles)
    elif alg == 1:
        print("Backtracking")
        BackTracking().get_algorithm_steps(tiles, variables, words)
    elif alg == 2:
        print("Backtracking + ForwardChecking")
        ForwardChecking().get_algorithm_steps(tiles, variables, words)
    # elif alg == 3:
    #     print("Get all arcs test")
    #     ArcConsistency().test(tiles, variables, words)
    
    # print(tiles)
    # print(words)
    # print(variables)