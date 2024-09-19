import unittest
from automathon import DFA


class TestDFA(unittest.TestCase):
    fa = DFA(
        q={"q0", "q1", "q2"},
        sigma={"0", "1"},
        delta={
            "q0": {"0": "q0", "1": "q1"},
            "q1": {"0": "q2", "1": "q0"},
            "q2": {"0": "q1", "1": "q2"},
        },
        initial_state="q0",
        f={"q0"},
    )

    dfa = DFA(
        q={"A", "B"},
        sigma={"0", "1"},
        delta={"A": {"0": "A", "1": "B"}, "B": {"0": "B", "1": "A"}},
        initial_state="A",
        f={"B"},
    )

    dfa_1 = DFA(
        q={"R", "S", "T", "U"},
        sigma={"0", "1"},
        delta={
            "R": {"0": "S", "1": "R"},
            "S": {"0": "T", "1": "R"},
            "T": {"0": "U", "1": "R"},
            "U": {"0": "U", "1": "U"},
        },
        initial_state="R",
        f={"U"},
    )

    dfa_ab = DFA(
        q={"1", "2"},
        sigma={"a", "b"},
        delta={"1": {"a": "2", "b": "1"}, "2": {"a": "1", "b": "2"}},
        initial_state="1",
        f={"1"},
    )

    dfa_ab_inv = DFA(
        q={"3", "4"},
        sigma={"a", "b"},
        delta={"3": {"a": "3", "b": "4"}, "4": {"a": "4", "b": "3"}},
        initial_state="3",
        f={"3"},
    )

    def test_is_valid(self):
        self.assertTrue(self.fa.is_valid())

    def test_accept_empty(self):
        self.assertTrue(self.fa.accept(""))

    def test_accept_str_1(self):
        self.assertTrue(self.fa.accept("001001"))

    def test_accept_str_2(self):
        self.assertTrue(self.fa.accept("0101010101010"))

    def test_complement(self):
        not_fa = self.fa.complement()
        self.assertFalse(not_fa.accept("001001"))

    def test_product(self):
        dfa = DFA(
            q={"A", "B"},
            sigma={"a", "b"},
            delta={"A": {"a": "B", "b": "A"}, "B": {"a": "A", "b": "B"}},
            initial_state="A",
            f={"A"},
        )

        dfa_1 = DFA(
            q={"C", "D"},
            sigma={"a", "b"},
            delta={"C": {"a": "C", "b": "D"}, "D": {"a": "D", "b": "C"}},
            initial_state="C",
            f={"C"},
        )

        product_result = dfa.product(dfa_1)

        self.assertTrue(product_result.is_valid())
        self.assertTrue(product_result.accept(""))
        self.assertTrue(product_result.accept("bb"))
        self.assertFalse(product_result.accept("b"))

    def test_product_1(self):
        product_result = self.dfa.product(self.dfa_1)

        self.assertTrue(product_result.is_valid())
        self.assertTrue(product_result.accept("0001"))
        self.assertFalse(product_result.accept("00010010"))

    def test_union(self):
        union_result = self.dfa.union(self.dfa_1)

        self.assertTrue(union_result.is_valid())
        self.assertTrue(union_result.accept("00010010"))
        self.assertTrue(union_result.accept("0011000"))

    def test_intersection(self):
        intersection_result = self.dfa.intersection(self.dfa_1)

        self.assertTrue(intersection_result.is_valid())
        self.assertTrue(intersection_result.accept("0001"))
        self.assertFalse(intersection_result.accept("00010010"))

    def test_difference(self):
        difference_result = self.dfa_ab.difference(self.dfa_ab_inv)

        self.assertTrue(difference_result.is_valid())
        self.assertTrue(difference_result.accept("b"))
        self.assertTrue(difference_result.accept("aba"))
        self.assertFalse(difference_result.accept("aa"))
        self.assertFalse(difference_result.accept("ab"))
        self.assertFalse(difference_result.accept("abbabb"))

    def test_symmetric_difference(self):
        symmetric_difference_result = self.dfa_ab.symmetric_difference(
            self.dfa_ab_inv
        )

        self.assertTrue(symmetric_difference_result.is_valid())
        self.assertTrue(symmetric_difference_result.accept("b"))
        self.assertTrue(symmetric_difference_result.accept("a"))
        self.assertFalse(symmetric_difference_result.accept("aa"))
        self.assertFalse(symmetric_difference_result.accept("ab"))
        self.assertFalse(symmetric_difference_result.accept("abbabb"))

    def test_minimize(self):
        dfa = DFA(
            q={"A", "B", "C", "D", "E", "F"},
            sigma={"0", "1"},
            delta={
                "A": {"0": "B", "1": "C"},
                "B": {"0": "A", "1": "D"},
                "C": {"0": "E", "1": "F"},
                "D": {"1": "F"},
                "E": {"0": "D", "1": "F"},
                "F": {"0": "F", "1": "F"},
            },
            initial_state="A",
            f={"D", "E"},
        )

        minimized_dfa = dfa.minimize()

        self.assertTrue(minimized_dfa.is_valid())
        self.assertGreaterEqual(len(dfa.q), len(minimized_dfa.q))

    def test_minimize_2(self):
        fa = DFA(
            q={"q0", "q1", "q2", "q3", "q4", "q5"},
            sigma={"0", "1"},
            delta={
                "q0": {"0": "q3", "1": "q1"},
                "q1": {"0": "q2", "1": "q5"},
                "q2": {"0": "q2", "1": "q5"},
                "q3": {"0": "q0", "1": "q4"},
                "q4": {"0": "q2", "1": "q5"},
                "q5": {"0": "q5", "1": "q5"},
            },
            initial_state="q0",
            f={"q1", "q2", "q4"},
        )
        minimized_fa = fa.minimize()

        self.assertGreaterEqual(len(fa.q), len(minimized_fa.q))
        self.assertEqual(fa.accept("1"), minimized_fa.accept("1"))
        self.assertEqual(fa.accept("11"), minimized_fa.accept("11"))
        self.assertEqual(fa.accept("110"), minimized_fa.accept("110"))
        self.assertEqual(fa.accept("1101"), minimized_fa.accept("1101"))
        self.assertEqual(fa.accept("01"), minimized_fa.accept("01"))
        self.assertEqual(fa.accept("0101"), minimized_fa.accept("0101"))

    def test_minimize_existing_1(self):
        fa = DFA(
            q={"q0", "q1", "q2"},
            sigma={"0", "1"},
            delta={
                "q0": {"0": "q0", "1": "q1"},
                "q1": {"0": "q2", "1": "q0"},
                "q2": {"0": "q1", "1": "q2"},
            },
            initial_state="q0",
            f={"q0"},
        )
        minimized_fa = fa.minimize()
        not_minimized_fa = minimized_fa.complement()

        self.assertGreaterEqual(len(fa.q), len(minimized_fa.q))
        self.assertTrue(minimized_fa.is_valid())
        self.assertEqual(fa.accept(""), minimized_fa.accept(""))
        self.assertEqual(fa.accept("001001"), minimized_fa.accept("001001"))
        self.assertEqual(
            fa.accept("0101010101010"), minimized_fa.accept("0101010101010")
        )

        self.assertTrue(not_minimized_fa.is_valid())
        self.assertFalse(not_minimized_fa.accept(""))
        self.assertFalse(not_minimized_fa.accept("001001"))
        self.assertFalse(not_minimized_fa.accept("0101010101010"))


if __name__ == "__main__":
    unittest.main()
