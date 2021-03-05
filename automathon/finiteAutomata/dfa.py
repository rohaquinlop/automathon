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

  def getInitialState(self):
      """Returns the initial state string
      """
    return self.initialState

  def isValid(self) -> bool:
    pass
