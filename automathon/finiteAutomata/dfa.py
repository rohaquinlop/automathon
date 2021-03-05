class DFA():
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
  """

  def __init__(self, Q : set, sigma : set, delta : dict, initialState : str, F : set):
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
    self.initialState = initialState
    self.sigma = sigma
    self.delta = delta
    self.initialState = initialState
    self.F = F

  def isValid(self) -> bool:
    """ Returns True if the DFA is an valid automata """

    #Validate if the initial state is in the set Q
    if self.initialState not in self.Q:
      return False

    #Validate if the delta transitions are in the set Q
    for d in self.delta:
      if d not in self.Q:
        return False

      #Validate if the d transitions are valid
      for s in self.delta[d]:
        if s not in self.sigma or self.delta[d][s] not in q:
          return False


    #Validate if the final state are in Q
    for f in self.F:
      if f not in self.Q:
        return False

    #None of the above cases failed then this DFA is valid
    return True

