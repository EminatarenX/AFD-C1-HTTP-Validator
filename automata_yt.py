import string

class DFA:
    def __init__ (self, states, alphabet, transition_function, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.final_states = final_states

    def accepts(self, input):
        current_state = self.start_state
        generated_string = ""

        for symbol in input:
            if symbol not in self.alphabet:
                return False, generated_string
            if current_state not in self.transition_function:
                return False, generated_string
            if symbol not in self.transition_function[current_state]:
                return False, generated_string
            current_state = self.transition_function[current_state][symbol]
            generated_string += symbol
        return current_state in self.final_states, generated_string.strip()

    def check_transitions(self, state):
        return self.transition_function.get(state, None)
        

states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q61', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30', 'q31', 'q32', 'q33', 'q56', 'q57', 'q58', 'q59', 'q60']
alphabet = set(string.ascii_lowercase + string.digits + 'G'+ 'E'+ 'T'+ '/' + ' '+ 'H'+ 'P'+'.'+'&'+'='+'?'+ 'O'+'S'+'U'+'A'+'C'+'D'+'L')
transition_function = {
    # Métodos HTTP
    'q0': {'G': 'q1', 'D': 'q17', 'P': 'q7', ' ': 'q0'},
    'q1': {'E': 'q2'}, 
    'q2': {'T': 'q3'},
    'q3': {' ': 'q4'}, 

    'q7': {'A': 'q8', 'U': 'q12', 'O': 'q14'},
    'q8': {'T': 'q9'},
    'q9': {'C': 'q10'},
    'q10': {'H': 'q11'},
    'q11': {' ': 'q4'},
    
    'q12': {'T': 'q13'},
    'q13': {' ': 'q4'},
    'q14': {'S': 'q15'},
    'q15': {'T': 'q16'},
    'q16': {' ': 'q4'},
    
    'q17': {'E': 'q18'},
    'q18': {'L': 'q19'},
    'q19': {'E': 'q20'},
    'q20': {'T': 'q21'},
    'q21': {'E': 'q22'},
    'q22':  {' ':  'q4'},
    
    # Path de la petición
    'q4': {' ': 'q4', '/': 'q61'},
    'q61': {**{char: 'q5' for char in string.ascii_lowercase + string.digits}},
    'q5': {**{char: 'q5' for char in string.ascii_lowercase + string.digits}, '/': 'q6', ' ': 'q23', '?': 'q56', '.': 'q34'},
    'q6': {**{char: 'q5' for char in string.ascii_lowercase + string.digits}},
    
    # Rutas estáticas y dinámicas
    'q34': {'j': 'q50', 'a': 'q47', 'p': 'q44', 'h': 'q35', 'c': 'q53'},
    'q50': {'s': 'q51', 'p': 'q42'},
    'q51': {'p': 'q52'},
    'q52': {'?': 'q56', ' ': 'q23'},
    'q47': {'s': 'q48'},
    'q48': {'p': 'q49'},
    'q49': {'?':  'q56', ' ':   'q23'},
    'q44': {'n': 'q45', 'h': 'q39'},
    'q45': {'g': 'q46'},
    'q46': {' ': 'q23'},
    'q42': {'g': 'q43'},
    'q43': {' ':'q23'},
    'q39': {'p': 'q40'},
    'q40': {'?': 'q56',' ': 'q23'},
    'q35': {'t': 'q36'},
    'q36': {'m': 'q37'},
    'q37': {'l': 'q101'},
    'q101': {' ':'q23'},
    'q53': {'s': 'q54'},
    'q54': {'s': 'q55'},
    
    # Query Parameters
    'q56': {**{char: 'q57' for char in string.ascii_lowercase + string.digits}},
    'q57': {**{char: 'q57' for char in string.ascii_lowercase + string.digits}, '=': 'q58'},
    'q58': {**{char: 'q59' for char in string.ascii_lowercase + string.digits}},
    'q59': {**{char: 'q59' for char in string.ascii_lowercase + string.digits}, '&': 'q60', ' ': 'q23'},
    'q60': {**{char: 'q57' for char in string.ascii_lowercase + string.digits}},
    
    # Version de http y estados finales
    'q23': {' ': 'q23', 'H': 'q24'},
    'q24': {'T': 'q25'},
    'q25': {'T': 'q26'},
    'q26': {'P': 'q27'},
    'q27': {'/': 'q28'},
    'q28': {'2': 'q33', '1': 'q29'},
    'q29': {'.': 'q30'},
    'q30': {'0': 'q31', '1': 'q32'},
    
}

start_state = 'q0'
final_states = ['q31', 'q32', 'q33']
dfa = DFA(states, alphabet, transition_function, start_state, final_states)

# Pruebas
test_strings = [
    # Peticiones válidas
    ' GET /aaaaaa/sdf HTTP/2',
    'GET /123/abc/456 HTTP/1.1',
    'GET /valid/path/with/multiple/segments HTTP/1.0',
    'GET /valid/path/user?value=2 HTTP/1.1',
    'GET /double/quer1/params?value1=2&value2=3 HTTP/1.0',
    'POST /new/resource HTTP/2',
    'PUT /update/data/123 HTTP/1.1',
    'DELETE /remove/item/42 HTTP/2',
    'PATCH /modify/resource/56 HTTP/1.1',
    'POST /submit/form HTTP/1.0',
    'PUT /update/profile HTTP/2',
    'DELETE /delete/account HTTP/1.1',
    'PATCH /edit/article HTTP/1.1',
    'GET  /submit/form.html HTTP/2',
    'POST /submit/form.php?user=emiliano&password=123 HTTP/1.1',
    
    # Peticiones inválidas
    'GET /invalid path',
    'POST /not/valid',
    'PUT /update//data// HTTP/1.1',
    'DELETE  /wrong/method/space HTTP/1.1',
    'PATCH no/slash/in/path HTTP/1.0',
    'GET /query?missing_equals&no_value HTTP/1.1',
    'POST missingpath HTTP/1.0',  # Falta la barra '/'
    'PUT /invalid/ path HTTP/1.1',  # Espacio en la ruta
    'DELETE /extra//slash/ HTTP/2',  # Barra extra en la ruta
]


for test in test_strings:
    result, generated_string = dfa.accepts(test)
    print(f"Input: '{test}'")
    print(f"Accepted: {result}, Generated String: '{generated_string}'")
    print()