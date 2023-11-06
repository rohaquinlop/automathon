import unittest
from automathon import NFA


class TestNFA(unittest.TestCase):
    fa = NFA(
        q={'q1', 'q2', 'q3', 'q4'},
        sigma={'0', '1'},
        delta={
            'q1': {
                '0': {'q1'},
                '1': {'q1', 'q2'}
            },
            'q2': {
                '0': {'q3'},
                '': {'q3'}
            },
            'q3': {
                '1': {'q4'},
            },
            'q4': {
                '0': {'q4'},
                '1': {'q4'},
            },
        },
        initial_state='q1',
        f={'q4'}
    )

    fa_1 = NFA(
        q={'3', '1', '2', '4', '0'},
        sigma={'', 'AA', 'BB', 'DD', 'CC'},
        delta={
            '0': {'AA': {'1'}},
            '1': {'BB': {'2'}},
            '2': {'CC': {'3'}},
            '3': {
                '': {'1'},
                'DD': {'4'}
            }
        },
        initial_state='0',
        f={'4'}
    )

    def test_isValid(self):
        self.assertTrue(self.fa.is_valid())

    def test_accept_str_1(self):
        self.assertTrue(self.fa.accept("000001100001"))

    def test_accept_str_2(self):
        self.assertTrue(self.fa.accept("0000011"))

    def test_accept_str_3(self):
        self.assertFalse(self.fa.accept("000001"))

    def test_remove_epsilon_transitions_1(self):
        no_epsilon_transitions = self.fa_1.remove_epsilon_transitions()
        self.assertTrue(no_epsilon_transitions.is_valid())

    def test_remove_epsilon_transitions_2(self):
        dfa = self.fa.get_dfa()
        self.assertFalse(dfa.accept("000001"))

    def test_remove_epsilon_transitions_3(self):
        dfa = self.fa.get_dfa()
        self.assertTrue(dfa.accept("0000011"))

    def test_nfa_dfa_1(self):
        dfa = self.fa_1.get_dfa()
        self.assertTrue(dfa.is_valid())

    def test_product(self):
        nfa = NFA(
            q={'A', 'B'},
            sigma={'a', 'b'},
            delta={
                'A': {
                    'a': {'B'},
                    'b': {'A'}
                },
                'B': {
                    'a': {'A'},
                    'b': {'B'}
                }
            },
            initial_state='A',
            f={'A'}
        )

        nfa_1 = NFA(
            q={'C', 'D'},
            sigma={'a', 'b'},
            delta={
                'C': {
                    'a': {'C'},
                    'b': {'D'}
                },
                'D': {
                    'a': {'D'},
                    'b': {'C'}
                }
            },
            initial_state='C',
            f={'C'}
        )

        product_result = nfa.product(nfa_1)

        self.assertTrue(product_result.is_valid())
        self.assertTrue(product_result.accept(""))
        self.assertTrue(product_result.accept("bb"))
        self.assertFalse(product_result.accept("b"))
        self.assertTrue(product_result.accept("bbaa"))
        self.assertFalse(product_result.accept("bbaaa"))

    def test_union(self):
        nfa = NFA(
            q={'A'},
            sigma={'a'},
            delta={
                'A': {
                    'a': {'A'}
                }
            },
            initial_state='A',
            f={'A'}
        )

        nfa_1 = NFA(
            q={'C', 'D', 'E'},
            sigma={'a', 'b'},
            delta={
                'C': {
                    'b': {'D'},
                },
                'D': {
                    'a': {'E'},
                    'b': {'D'}
                }
            },
            initial_state='C',
            f={'E'}
        )

        union_result = nfa.union(nfa_1)

        self.assertTrue(union_result.is_valid())
        self.assertTrue(union_result.accept("aaaaaa"))
        self.assertTrue(union_result.accept("bbbbbbbbba"))
        self.assertFalse(union_result.accept("aaaabbbbaaa"))
        self.assertFalse(union_result.accept("aaaaaaaab"))

    def test_renumber(self):
        from automathon import DFA

        automata_1 = NFA(
            q={'3', '1', '2', '0'},
            sigma={'', 'A', 'B', 'C'},
            delta={
                '0': {
                    'A': {'1'}
                },
                '1': {
                    'B': {'2'},
                    '': {'2'}
                },
                '2': {
                    'C': {'3'}
                }
            },
            initial_state='0',
            f={'3'}
        )

        automata_2: NFA = automata_1.remove_epsilon_transitions()
        automata_3: DFA = automata_2.get_dfa()
        automata_4: NFA = automata_3.get_nfa()

        automata_4.renumber()

        self.assertTrue(automata_4.is_valid())


if __name__ == '__main__':
    unittest.main()
