#!/usr/bin/env python
# coding: utf-8

# # NFA to DFA Converter

# 
# ## Step 1: Define the NFA

# In[1]:


nfa = {
    'states': {'q0', 'q1', 'q2'},
    'symbols': {'a', 'b'},
    'start': 'q0',
    'accept': {'q2'},
    'transitions': {
        ('q0', 'a'): {'q0', 'q1'},
        ('q1', 'b'): {'q2'}
    }
}


# ## Step 2: Define Conversion Function
# 

# In[2]:


from collections import defaultdict

def nfa_to_dfa(nfa):
    states = nfa['states']
    symbols = nfa['symbols']
    start = nfa['start']
    accept = nfa['accept']
    transitions = nfa['transitions']
    
    # Initialize DFA
    dfa_states = []
    dfa_transitions = {}
    unmarked_states = []
    
    # Start state of DFA (as a set of NFA states)
    start_state = frozenset([start])
    dfa_states.append(start_state)
    unmarked_states.append(start_state)
    
    # Subset Construction Algorithm
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
    
    # Find accept states
    dfa_accept = [state for state in dfa_states if state & accept]
    
    # Build DFA dictionary
    dfa = {
        'states': dfa_states,
        'symbols': symbols,
        'start': start_state,
        'accept': dfa_accept,
        'transitions': dfa_transitions
    }
    
    return dfa


# ## Step 3: Convert NFA to DFA and display results
# 

# In[3]:


dfa = nfa_to_dfa(nfa)

print("NFA States:", nfa['states'])
print("NFA Start State:", nfa['start'])
print("NFA Accept States:", nfa['accept'])
print("\nDFA States:", dfa['states'])
print("DFA Start State:", dfa['start'])
print("DFA Accept States:", dfa['accept'])
print("\nDFA Transitions:")
for (state, symbol), next_state in dfa['transitions'].items():
    print(f"  δ({set(state)}, '{symbol}') -> {set(next_state)}")


# In[ ]:




