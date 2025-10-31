import streamlit as st
from collections import defaultdict

st.title("🔁 NFA → DFA Converter")

st.write("""
This app converts a Non-Deterministic Finite Automaton (NFA) into an equivalent 
Deterministic Finite Automaton (DFA) using the Subset Construction Algorithm.
""")

# --- Input fields ---
states = st.text_input("Enter NFA States (comma separated)", "q0,q1,q2")
symbols = st.text_input("Enter Input Symbols (comma separated)", "a,b")
start_state = st.text_input("Enter Start State", "q0")
accept_states = st.text_input("Enter Accept States (comma separated)", "q2")
transitions_text = st.text_area(
    "Enter Transitions (format: q0,a->q0 q1 per line)",
    "q0,a->q0 q1\nq1,b->q2"
)

# --- Convert NFA to dictionary ---
def parse_nfa(states, symbols, start, accept, transitions_text):
    transitions = {}
    for line in transitions_text.strip().splitlines():
        if "->" in line:
            left, right = line.split("->")
            state, symbol = left.split(",")
            transitions[(state.strip(), symbol.strip())] = set(right.strip().split())
    nfa = {
        'states': set(states.split(",")),
        'symbols': set(symbols.split(",")),
        'start': start.strip(),
        'accept': set(accept.split(",")),
        'transitions': transitions
    }
    return nfa

# --- Conversion algorithm ---
def nfa_to_dfa(nfa):
    states = nfa['states']
    symbols = nfa['symbols']
    start = nfa['start']
    accept = nfa['accept']
    transitions = nfa['transitions']
    
    dfa_states = []
    dfa_transitions = {}
    unmarked_states = []
    
    start_state = frozenset([start])
    dfa_states.append(start_state)
    unmarked_states.append(start_state)
    
    while unmarked_states:
        current = unmarked_states.pop()
        for symbol in symbols:
            new_state = set()
            for nfa_state in current:
                if (nfa_state, symbol) in transitions:
                    new_state.update(transitions[(nfa_state, symbol)])
            new_state = frozenset(new_state)
            
            if new_state:
                dfa_transitions[(current, symbol)] = new_state
                if new_state not in dfa_states:
                    dfa_states.append(new_state)
                    unmarked_states.append(new_state)
    
    dfa_accept = [state for state in dfa_states if state & accept]
    
    dfa = {
        'states': dfa_states,
        'symbols': symbols,
        'start': start_state,
        'accept': dfa_accept,
        'transitions': dfa_transitions
    }
    return dfa

# --- Run conversion when button is pressed ---
if st.button("Convert to DFA"):
    nfa = parse_nfa(states, symbols, start_state, accept_states, transitions_text)
    dfa = nfa_to_dfa(nfa)
    
    st.subheader("✅ DFA Result")
    st.write("**States:**", dfa['states'])
    st.write("**Start State:**", dfa['start'])
    st.write("**Accept States:**", dfa['accept'])
    st.write("**Transitions:**")
    for (state, symbol), next_state in dfa['transitions'].items():
        st.write(f"δ({set(state)}, '{symbol}') → {set(next_state)}")
