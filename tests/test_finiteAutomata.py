import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pythomata.finiteAutomata.dfa import *

def test_dfa():
  fa = DFA(initialState='q0')

  assert fa.getInitialState() == 'q0'