import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pythomata.finiteAutomata import dfa

def test_dfa():
  fa = dfa.DFA(initialState='q0')

  assert fa.getInitialState() == 'q0'