# Exceptions module
from automathon.errors.errors import *
from collections import deque
from graphviz import Digraph


class DFA:
  """A Class used to represent a Deterministic Finite Automaton

  ...

  Attributes
  - - - - - - - - - - - - - - - - - -
  Q : set
    Set of strings where each string represent the states.
    Ex:
      Q = {'q0', 'q1', 'q2'}

  sigma : set
    Set of strings that represents the alphabet.
    Ex:
      sigma = {'0', '1'}
  
  delta : dict
    Dictionary that represents the transition function.
    Ex:
      delta = {
                'q0' : {'0' : 'q0', '1' : 'q1'},
                'q1' : {'0' : 'q2', '1' : 'q0'},
                'q2' : {'0' : 'q1', '1' : 'q2'},
              }
  
  initialState : str
    String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).
    Ex:
      initialState = 'q0'
  
  F : set
    Set of strings that represent the final state/states of Q (F ⊆ Q).
    Ex:
      F = {'q0'}
  

  Methods
  - - - - - - - - - - - - - - - - - -

  isValid() -> bool : Returns True if the DFA is a valid automata
  accept(S : str) -> bool : Returns True if the given string S is accepted by the DFA
  complement() -> DFA : Returns the complement of the DFA
  """
  
  def __init__(self, Q: set, sigma: set, delta: dict, initialState: str, F: set):
    """
    Parameters
    - - - - - - - - - - - - - - - - - -
    
    Q : set
      Set of strings where each string represent the states.
    
    sigma : set
      Set of strings that represents the alphabet.
    
    delta : dict
      Dictionary that represents the transition function.
    
    initialState : str
      String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).
    
    F : set
      Set of strings that represent the final state/states of Q (F ⊆ Q).
    """
    self.Q = Q
    self.sigma = sigma
    self.delta = delta
    self.initialState = initialState
    self.F = F
  
  def accept(self, S: str) -> bool:
    """ Returns True if the given string S is accepted by the DFA

    The string S will be accepted if ∀a · a ∈ S ⇒ a ∈ sigma, which means that all the characters in S must be in sigma (must be in the alphabet).

    Parameters
    - - - - - - - - - - - - - - - - - -
    S : str
      A string that the DFA will try to process.
    """
    
    ## Basic Idea: Search through states (delta) in the DFA, since the initial state to the final states
    
    ## BFS states
    
    q = deque()  ## queue -> states from i to last character in S | (index, state)
    q.append([0, self.initialState])  ## Starts from 0
    ans = False  ## Flag
    
    while q and not ans:
      frontQ = q.popleft()
      idx = frontQ[0]
      state = frontQ[1]
      
      if idx == len(S):
        if state in self.F:
          ans = True
      elif S[idx] not in self.sigma:
        raise InputError(S[idx], 'Is not declared in sigma')
      elif state in self.delta:
        ## Search through states
        for transition in self.delta[state].items():
          ## transition = ('1', 'q0')
          if S[idx] == transition[0]:
            q.append([idx + 1, transition[1]])
    
    if S == "":
      ans = True
    
    return ans
  
  def isValid(self) -> bool:
    """ Returns True if the DFA is an valid automata """
    
    # Validate if the initial state is in the set Q
    if self.initialState not in self.Q:
      raise SigmaError(self.initialState, 'Is not declared in Q')
    
    # Validate if the delta transitions are in the set Q
    for d in self.delta:
      if d not in self.Q:
        raise SigmaError(d, 'Is not declared in Q')
      
      # Validate if the d transitions are valid
      for s in self.delta[d]:
        if s not in self.sigma:
          raise SigmaError(s, 'Is not declared in sigma')
        elif self.delta[d][s] not in self.Q:
          raise SigmaError(self.delta[d][s], 'Is not declared Q')
    
    # Validate if the final state are in Q
    for f in self.F:
      if f not in self.Q:
        raise SigmaError(f, 'Is not declared in Q')
    
    # None of the above cases failed then this DFA is valid
    return True
  
  def complement(self) -> 'DFA':
    """Returns the complement of the DFA."""
    Q = self.Q
    sigma = self.sigma
    delta = self.delta
    initialState = self.initialState
    F = {state for state in self.Q if state not in self.F}
    
    return DFA(Q, sigma, delta, initialState, F)
  
  def getNFA(self):
    from automathon.finiteAutomata.nfa import NFA
    """Convert the actual DFA to NFA class and return it's conversion"""
    ##TODO: Add to documentation
    Q = self.Q.copy()
    delta = dict()
    initialState = self.initialState
    F = self.F.copy()
    sigma = self.sigma
    
    for state, transition in self.delta.items():
      ## state : str, transition : dict(sigma, Q)
      tmp = dict()
      for s, q in transition.items():
        ## s : sigma
        tmp[s] = [''.join(q)]
      
      delta[state] = tmp
    
    return NFA(Q, sigma, delta, initialState, F)
  
  def product(self, M: 'DFA') -> 'DFA':
    """Given a DFA M returns the product automaton"""
    ##TODO: Add to documentation
    delta = dict()
    Q = set()
    F = set()
    sigma = self.sigma.intersection(M.sigma)
    
    for state, transition in self.delta.items():
      ## i : str, j : dict(sigma, Q)
      for stateM, transitionM in M.delta.items():
        ## stateM : str, transitionM : dict(sigma, Q)
        for s in transition:
          if s in transitionM:
            ## sigma value in common
            sigma.add(s)
            
            tmp = str([state, stateM])
            tmp1 = str([transition[s], transitionM[s]])
            aux = dict()
            aux[s] = tmp1
            
            Q.add(tmp)
            Q.add(tmp1)
            
            if state in self.F and stateM in M.F:
              F.add(tmp)
            
            if transition[s] in self.F and transitionM[s] in M.F:
              F.add(tmp1)
            
            if tmp in delta:
              delta[tmp].update(aux)
            else:
              delta[tmp] = aux
    
    return DFA(Q, sigma, delta, str([self.initialState, M.initialState]), F)
  
  def union(self, M: 'DFA') -> 'DFA':
    """Given a DFA M returns the union automaton"""
    ##TODO: Add to documentation
    tmpNFA = self.getNFA()
    tmpNFA = tmpNFA.union(M.getNFA()).removeEpsilonTransitions()
    
    return tmpNFA.getDFA()
  
  def view(self, fileName: str):
    dot = Digraph(name=fileName, format='png')
    
    dot.graph_attr['rankdir'] = 'LR'
    
    dot.node("", "", shape='plaintext')
    
    for f in self.F:
      dot.node(f, f, shape='doublecircle')
    
    for q in self.Q:
      if q not in self.F:
        dot.node(q, q, shape='circle')
    
    dot.edge("", self.initialState, label="")
    
    for q in self.delta:
      for s in self.delta[q]:
        dot.edge(q, self.delta[q][s], label=s)
    
    dot.render()
