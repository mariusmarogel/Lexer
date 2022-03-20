import itertools
from classes import DFA

def runlexer(in_lex, input, outp):
    out = open(outp, "w+")
    lex = open(in_lex, "r")
    inp = open(input, "r")
    content_lex = lex.read()
    content_lex = content_lex.split('\n')
    word = inp.read()
    dfa_list = []
    while content_lex:
        count_trans = 0
        name = str(content_lex[1]) 
        alphabet_set = set(content_lex[0]) 
        alphabet = set()
        states_set = set()
        initial_state = int(content_lex[2]) 
        final_states = []
        if name == "NEWLINE":
            alphabet_set.clear()
            alphabet_set.add('\n')
        for elem in content_lex[3:]:
            if name == "NEWLINE" and len(elem) >= 2:
                states_set.add(int(elem[0]))
                states_set.add(int(elem[7]))
                count_trans += 1
            else:
                length = len(elem)
                if length <= 1:
                    break
                index = elem.find(',')
                if index == -1:
                    break
                states_set.add(int(elem[0:index]))
                string = ""
                for x in elem[(index + 5):]:
                    string = string + x
                states_set.add(int(string))
                count_trans += 1
        content_lex[(3 + count_trans)] = content_lex[(3 + count_trans)].split(' ')
        for x in content_lex[(3 + count_trans)]:
           final_states.append(int(x))
        alphabet = sorted(alphabet_set)
        tuples = itertools.product(states_set, alphabet)
        deltafunc = dict.fromkeys(tuples)
        for elem in content_lex[3:]:
            if name == "NEWLINE" and len(elem) >= 2:
                deltafunc[(int(elem[0]), '\n')] = int(elem[7])
            else:
                length = len(elem)
                if length <= 1:
                    break
                if isinstance(elem, list):
                    break
                index = elem.find(',')
                if index == -1:
                    break
                deltafunc[(int(elem[0:index]), elem[index + 2])] = int(elem[(index + 5):])
        for x in deltafunc:
            if deltafunc[x] is None:
                deltafunc[x] = x[0]
        
        A = DFA(alphabet, name, deltafunc, initial_state, final_states)
        A.sink_states()
        dfa_list.append(A)
        content_lex = content_lex[(3 + count_trans + 2):]
    copy = word
    debris = 0
    n = len(dfa_list)
    output = ""
    idx_acc = 0
    sum_acc = 0
    while copy:
        ch = copy[0]
        debris = 0
        string = ""
        token = ""
        idx = 0    
        states = [dfa_list[i].initial_state for i in range(n)]
        current_states = ['' for i in range(n)]
        for i in range(n):
            if ch not in dfa_list[i].alphabet:
                states[i] = None
            else:
                states[i] = dfa_list[i].delta_function[(dfa_list[i].initial_state), ch]
        current_states = check_curr(dfa_list, states, current_states)
        while not check_continue(current_states):
            for elem in current_states:
                if elem == 'a':
                    debris = len(string) + 1
                    idx_acc = debris
                    token = dfa_list[current_states.index(elem)].name
            string = string + ch
            idx += 1
            if idx >= len(copy):
                break
            ch = copy[idx]
            for i in range(n):
                if ch not in dfa_list[i].alphabet:
                    states[i] = None
                elif states[i] is not None:
                    states[i] = dfa_list[i].delta_function[(states[i], ch)]
            current_states = check_curr(dfa_list, states, current_states)
        if debris == 0:
            if idx_acc + sum_acc > len(word):
                output = "No viable alternative at character EOF, line 0"
                break
            else:
                output = "No viable alternative at character " + str(idx_acc + sum_acc) + ", line 0"
                break
        elif string == "\n":
            output = output + token + " " + "\\n" + "\n"
        else:
            output = output + token + " " + string[:debris] + "\n"
            sum_acc = sum_acc + len(string[:debris])
        copy = copy[debris:]
    if debris == 0:
        out.write(output)
    else:
        out.write(output[:-1])
    #print(output)
    lex.close()
    inp.close()
    out.close()

def check_curr(dfa_list, states, current_states):
    dfa_number = len(dfa_list)
    for i in range(dfa_number):
        if current_states[i] == 'r':
            continue
        if states[i] in dfa_list[i].final_states:
            current_states[i] = 'a'
        elif states[i] == dfa_list[i].sink_state or states[i] is None:
            current_states[i] = 'r'
        else:
            current_states[i] = 's'
    return current_states

def check_continue(current_states):
    for elem in current_states:
        if elem == 'a' or elem == 's':
            return False
    return True