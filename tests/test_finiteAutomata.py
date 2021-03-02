import pythomata.finiteAutomata.dfa as pydfa

def test_dfa():
  fa = pydfa.DFA(initialState='q0')

  assert fa.getInitialState() == 'q0'