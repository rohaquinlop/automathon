from pythomata.finiteAutomata import dfa

def test_dfa():
  fa = dfa.DFA(initialState='q0')

  assert fa.getInitialState() == 'q0'