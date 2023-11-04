# Exceptions module
from automathon.errors.errors import *
from collections import deque
from graphviz import Digraph
from automathon.finiteAutomata.dfa import DFA


class NFA:
    """A Class used to represent a Non-Deterministic Finite Automaton

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
                'q0' : {
                        '0' : {'q0', 'q2'},
                        '1' : {'q1', 'q2', 'q3'}
                       },
                'q1' : {
                        '0' : {'q2'},
                        '1' : {'q0', 'q1'}
                       },
                'q2' : {
                        '0' : {'q1', 'q2'},
                        '' : {'q2'}
                       },
              }
  
  initialState : str
    String that represents the initial state from where any input is processed (initialState ∈ Q / initialState in Q).
    Ex:
      initialState = 'q0'
  
  F : set
    Set of strings that represent the final state/states of Q (F ⊆ Q).
    Ex:
      F = {'q0', 'q1'}
  

  Methods
  - - - - - - - - - - - - - - - - - -

  isValid() -> bool : Returns True if the NFA is a valid automata
  accept(S : str) -> bool : Returns True if the given string S is accepted by the NFA
  complement() -> NFA : Returns the complement of the NFA
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
        """ Returns True if the given string S is accepted by the NFA

    The string S will be accepted if ∀a · a ∈ S ⇒ a ∈ sigma, which means that all the characters in S must be in sigma
    (must be in the alphabet).

    Parameters
    - - - - - - - - - - - - - - - - - -
    S : str
      A string that the NFA will try to process.
    """

        # Basic Idea: Search through states (delta) in the NFA, since the initial state to the final states

        # BFS states

        q = deque()  # queue -> states from i to last character in S | (index, state)
        q.append([0, self.initialState])  # Starts from 0
        ans = False  # Flag

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
                # Search through states
                for transition in self.delta[state].items():
                    d = transition[0]
                    states = transition[1]

                    if d == "":
                        # Is epsilon
                        for state in states:
                            # Do not consume character
                            q.append([idx, state])
                    elif S[idx] == d:
                        for state in states:
                            # Consume character
                            q.append([idx + 1, state])

        if S == "":
            ans = True

        return ans

    def is_valid(self) -> bool:
        """ Returns True if the NFA is a valid automata """
        ans = True
        not_declared_state = None

        # Validate if the initial state is in the set Q
        if self.initialState not in self.Q:
            not_declared_state = self.initialState

        # Validate if the delta transitions are in the set Q
        for d in self.delta:
            if not_declared_state is not None:
                break

            if d != "" and d not in self.Q:
                not_declared_state = d

            # Validate if the d transitions are valid
            for s in self.delta[d]:
                if s != "" and s not in self.sigma:
                    not_declared_state = s
                for q in self.delta[d][s]:
                    if q not in self.Q:
                        not_declared_state = self.delta[d][s]

        # Validate if the final state are in Q
        for f in self.F:
            if f not in self.Q:
                not_declared_state = f

        if not_declared_state is not None:
            raise SigmaError(not_declared_state, 'Is not declared in Q')
        return ans

    def complement(self) -> 'NFA':
        """Returns the complement of the NFA."""
        Q = self.Q
        sigma = self.sigma
        delta = self.delta
        initialState = self.initialState
        F = {state for state in self.Q if state not in self.F}

        return NFA(Q, sigma, delta, initialState, F)

    def get_e_closure(self, q, visited=None):
        """Returns a list of the epsilon closures from estate q"""
        ans = [q]
        if visited is None:
            visited = list(q)

        if q in self.delta:
            if '' in self.delta[q]:
                for st in self.delta[q]['']:
                    if st not in visited:
                        visited.append(st)
                        ans.extend([k for k in self.get_e_closure(st, visited) if k not in ans])
        return ans

    def contains_epsilon_transitions(self) -> bool:
        """Returns True if the NFA contains Epsilon transitions else returns False"""
        for q in self.delta:
            if '' in self.delta[q]:
                return True
        return False

    def remove_epsilon_transitions(self) -> 'NFA':
        """Returns a copy of the actual NFA that doesn't contain epsilon transitions"""
        Qprime = self.Q.copy()
        deltaPrime = self.delta.copy()
        deltaInitState = self.initialState
        deltaF = self.F.copy()

        if self.contains_epsilon_transitions():
            deltaPrime = dict()
            for q in Qprime:
                closure_states = self.get_e_closure(q)

                for sigma in self.sigma:
                    toEpsiClosure = list()
                    newTransitions = list()

                    # Get the transitions from sigma in each epsilon closure
                    for closureState in closure_states:
                        if closureState in self.F:
                            deltaF.add(q)
                        if closureState in self.delta and sigma in self.delta[closureState]:
                            toEpsiClosure.extend(self.delta[closureState][sigma])

                    # Get the new transitions from the epsilon closure
                    for epsiClosure in toEpsiClosure:
                        newTransitions.extend(self.get_e_closure(epsiClosure))

                    if q not in deltaPrime:
                        deltaPrime[q] = dict()

                    if sigma != '':
                        deltaPrime[q][sigma] = set(newTransitions)

        return NFA(Qprime, self.sigma, deltaPrime, deltaInitState, deltaF)

    def get_dfa(self) -> DFA:
        """Convert the actual NFA to DFA and return its conversion"""

        local_nfa = NFA(self.Q, self.sigma, self.delta, self.initialState, self.F)
        local_nfa = local_nfa.remove_epsilon_transitions()

        Qprime = []
        deltaPrime = dict()

        queue = deque()
        visited = [[local_nfa.initialState]]
        queue.append([local_nfa.initialState])

        while queue:
            qs = queue.pop()  # state Q

            T = dict()  # {str : list}

            for q in qs:
                if q in local_nfa.delta:
                    for s in local_nfa.delta[q]:
                        tmp = local_nfa.delta[q][s].copy()
                        if tmp:
                            if s in T:
                                # avoid add repeated values
                                T[s].extend([k for k in tmp if k not in T[s]])
                            else:
                                T[s] = list(tmp)

            for t in T:
                T[t].sort()
                tmp = T[t].copy()
                if tmp not in visited:
                    queue.append(tmp)
                    visited.append(tmp)
                T[t] = str(T[t])

            deltaPrime[str(qs)] = T
            Qprime.append(qs)

        Fprime = set()

        for qs in Qprime:
            for q in qs:
                if q in local_nfa.F:
                    Fprime.add(str(qs))
                    break

        aux = set()

        for qs in Qprime:
            aux.add(str(qs))

        Qprime = aux

        return DFA(Qprime, local_nfa.sigma, deltaPrime, str([local_nfa.initialState]), Fprime)

    def minimize(self):
        """Minimize the automata and return the NFA result of the minimization"""
        localDFA = self.get_dfa()
        localNFA = localDFA.get_nfa()
        localNFA.renumber()
        return localNFA

    def renumber(self):
        """Change the name of the states, renumbering each of the labels"""
        idx = 0
        newTags = dict()

        # New values
        Q = set()
        delta = dict()
        F = set()

        # Setting the new label for each state
        tmpQ = list(self.Q)
        tmpQ.sort()

        for q in tmpQ:
            newTags[q] = str(idx)
            Q.add(str(idx))
            idx += 1

        initial_state = newTags[self.initialState]

        # Changing the labels for the final states
        for f in self.F:
            F.add(newTags[f])

        for q in self.delta:
            delta[newTags[q]] = dict()
            for s in self.delta[q]:
                nxtStates = list()
                for nxtState in self.delta[q][s]:
                    nxtStates.append(newTags[nxtState])

                delta[newTags[q]][s] = set(nxtStates)

        self.Q, self.F, self.delta, self.initialState = Q, F, delta, initial_state

    def union(self, M: 'NFA') -> 'NFA':
        """Given a NFA M returns the union automaton"""
        sigma = self.sigma.union(M.sigma)
        Q = set()
        F = set()
        initialState = "q0"
        Q.add(initialState)
        realValueSelf = dict()
        realValueM = dict()
        selfDelta = dict()
        mDelta = dict()
        # Fix possible errors when using the dictionaries with the name of the states
        for i, q in enumerate(self.Q, 1):
            realValueSelf[q] = "q{}".format(i)
            Q.add(realValueSelf[q])

        for i, s in enumerate(M.Q):
            realValueM[s] = "s{}".format(i)
            Q.add(realValueM[s])

        for q in self.F:
            F.add(realValueSelf[q])

        for q in M.F:
            F.add(realValueM[q])

        # Replace the values
        for q, transition in self.delta.items():
            # q : string, transition : {string -> list(string)}
            tmpDict = dict()
            for s, states in transition.items():
                tmpStates = []
                for state in states:
                    tmpStates.append(realValueSelf[state])

                tmpDict[s] = set(tmpStates.copy())
            selfDelta[realValueSelf[q]] = tmpDict.copy()

        for q, transition in M.delta.items():
            # q : string, transition : {string -> list(string)}
            tmpDict = dict()
            for s, states in transition.items():
                tmpStates = []
                for state in states:
                    tmpStates.append(realValueM[state])

                tmpDict[s] = set(tmpStates.copy())
            mDelta[realValueM[q]] = tmpDict.copy()

        delta = {**selfDelta, **mDelta, initialState: {
            '': {realValueSelf[self.initialState], realValueM[M.initialState]}}}

        return NFA(Q, sigma, delta, initialState, F)

    def product(self, M: 'NFA') -> 'NFA':
        """Given a DFA M returns the product automaton"""
        # Using DFA conversion
        a = self.get_dfa()
        b = M.get_dfa()

        nfa = a.product(b).get_nfa()

        return nfa

    def view(self, file_name: str):
        dot = Digraph(name=file_name, format='png')

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
                for t in self.delta[q][s]:
                    if s == '':
                        dot.edge(q, t, label='ε')
                    else:
                        dot.edge(q, t, label=s)

        dot.render()
