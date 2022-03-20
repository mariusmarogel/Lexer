class DFA:
    def __init__(self, alphabet, name, delta_function, initial_state, final_states):
        self.alphabet = alphabet
        self.name = name
        self.delta_function = delta_function
        self.initial_state = initial_state
        self.final_states = final_states
        self.sink_state = 0
    
    def next(self, tuplex):
        return (self.delta_function[(tuplex[0], tuplex[1][0])], tuplex[1][1:])
    
    def accepted(self, word):
        cnt = 0
        state = 0
        while cnt < len(word):
            state = self.next((state, word[cnt:]))[0]
            cnt += 1
        if state in self.final_states:
            return True
        else:
            return False
    
    def sink_states(self):
        #create states
        states = set()
        for x in self.delta_function:
            states.add(x[0])
        #check for sink-state and return it 
        for state in states:
            ok = 1
            for letter in self.alphabet:
                if(self.delta_function[(state, letter)] != state):
                    ok = 0
            if(ok == 1):
                self.sink_state = state
        