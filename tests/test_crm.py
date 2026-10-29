"""Tests of the CRM module (Member C). Do not edit.

Run them all:        python -m unittest tests.test_crm -v
Run one task only:   python -m unittest tests.test_crm -k crm03 -v
"""

import types
import unittest
from datetime import date

from erp.common.todo import require_enum
from erp.crm import algorithms as algo
from erp.crm import concepts as c
from erp.crm.data import load_leads, load_monthly_margins, load_offers, load_template
from erp.crm.models import Lead


def lead(lid: int, company: str = "Acme", stage: str = "new", revenue: float = 1000, probability: int = 10,
         salesperson: str = "lea", email: str = "x@acme.com", created: date = date(2026, 3, 1)) -> Lead:
    return Lead(lid, "Jo Doe", company, email, stage, revenue, probability, salesperson, created)


class TestCrm01Stages(unittest.TestCase):
    def setUp(self):
        require_enum(c.LeadStage, "CRM-01")

    def test_crm01_members_match_the_data(self):
        self.assertEqual([s.value for s in c.LeadStage], ["new", "qualified", "proposition", "won", "lost"])
        self.assertIs(c.LeadStage("won"), c.LeadStage.WON)
        with self.assertRaises(ValueError):
            c.LeadStage("negotiation")

    def test_crm01_default_probability(self):
        self.assertEqual([s.default_probability for s in c.LeadStage], [10, 30, 60, 100, 0])

    def test_crm01_is_open(self):
        self.assertEqual([s.is_open for s in c.LeadStage], [True, True, True, False, False])


class TestCrm02Comprehensions(unittest.TestCase):
    def test_crm02_split_contact_name(self):
        self.assertEqual(c.split_contact_name("Jean Dupont"), ("Jean", "Dupont"))
        self.assertEqual(c.split_contact_name("Jean-Marc  de la Fontaine"), ("Jean-Marc", "Fontaine"))
        self.assertEqual(c.split_contact_name("  Cher "), ("Cher", ""))
        with self.assertRaises(ValueError):
            c.split_contact_name("   ")

    def test_crm02_email_domains(self):
        leads = [lead(1, email="a@Acme.COM"), lead(2, email="b@acme.com"), lead(3, email=""), lead(4, email="c@x.be")]
        self.assertEqual(c.email_domains(leads), {"acme.com", "x.be"})
        real = c.email_domains(load_leads())
        self.assertIn("northwind.eu", real)
        self.assertIn("helio-energy.com", real)


class TestCrm03MapFilterZip(unittest.TestCase):
    def test_crm03_row_to_dict(self):
        self.assertEqual(c.row_to_dict(["id", "company"], [" 7", "Helio Energy "]), {"id": "7", "company": "Helio Energy"})
        with self.assertRaises(ValueError):
            c.row_to_dict(["id", "company"], ["7"])

    def test_crm03_weighted_pipeline(self):
        leads = [lead(1, "C", revenue=1000, probability=30), lead(2, "E", "won", 9999, 100),
                 lead(3, "B", revenue=500, probability=60), lead(4, "A", revenue=2000, probability=10),
                 lead(5, "D", "lost", 5000, 0), lead(6, "F", revenue=333, probability=33)]
        self.assertEqual(c.weighted_pipeline(leads), [("B", 300.0), ("C", 300.0), ("A", 200.0), ("F", 109.89)])
        self.assertEqual(c.weighted_pipeline(load_leads())[0], ("Helio Energy", 19800.0))


class TestCrm04Generators(unittest.TestCase):
    def test_crm04_valid_leads(self):
        leads = [lead(1, email="a@acme.com"), lead(2, email=""), lead(3, email="tom@atelierpeeters"),
                 lead(4, email="claire@@wavre.be"), lead(5, email="@acme.com"), lead(6, email="ok@x.be")]
        result = c.valid_leads(leads)
        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual([l.id for l in result], [1, 6])
        self.assertEqual(len(list(c.valid_leads(load_leads()))), 11)

    def test_crm04_all_leads(self):
        a, b, d = lead(1), lead(2), lead(3)
        result = c.all_leads([a], [], (x for x in [b, d]))
        self.assertIsInstance(result, types.GeneratorType)
        self.assertEqual(list(result), [a, b, d])
        self.assertEqual(list(c.all_leads()), [])


class TestCrm05Collections(unittest.TestCase):
    def test_crm05_leads_per_salesperson(self):
        leads = [lead(1, salesperson="lea"), lead(2, salesperson="karim"), lead(3, salesperson="karim"), lead(4, salesperson="max")]
        self.assertEqual(c.leads_per_salesperson(leads), [("karim", 2), ("lea", 1), ("max", 1)])
        self.assertEqual(c.leads_per_salesperson(load_leads()), [("sophie", 5), ("karim", 5), ("lea", 4)])

    def test_crm05_companies_with_multiple_leads(self):
        self.assertEqual(c.companies_with_multiple_leads(load_leads()),
                         {"Brightside Dental": [2, 7, 14], "Northwind Logistics": [4, 9]})
        self.assertEqual(c.companies_with_multiple_leads([lead(1, "A"), lead(2, "B")]), {})


class TestCrm06Itertools(unittest.TestCase):
    def test_crm06_assign_round_robin(self):
        self.assertEqual(c.assign_round_robin([21, 22, 23], ["lea", "karim"]), {21: "lea", 22: "karim", 23: "lea"})
        self.assertEqual(c.assign_round_robin([], ["lea"]), {})
        with self.assertRaises(ValueError):
            c.assign_round_robin([1], [])

    def test_crm06_leads_per_month(self):
        self.assertEqual(c.leads_per_month(load_leads()), [("2026-01", 3), ("2026-02", 5), ("2026-03", 6)])
        self.assertEqual(c.leads_per_month([lead(1, created=date(2025, 12, 31)), lead(2, created=date(2026, 1, 1))]),
                         [("2025-12", 1), ("2026-01", 1)])


class TestCrm07HeapBisect(unittest.TestCase):
    def test_crm07_top_opportunities(self):
        self.assertEqual(c.top_opportunities(load_leads(), 3), [10, 12, 4])
        leads = [lead(1, revenue=10), lead(2, stage="won", revenue=999), lead(3, revenue=30)]
        self.assertEqual(c.top_opportunities(leads, 5), [3, 1])

    def test_crm07_temperature(self):
        self.assertEqual([c.temperature(s) for s in (0, 39, 40, 69, 70, 100)],
                         ["cold", "cold", "warm", "warm", "hot", "hot"])


class TestCrm08Functools(unittest.TestCase):
    def test_crm08_company_key_is_cached(self):
        self.assertEqual(c.company_key("Lumen Consulting SA"), "lumen consulting")
        self.assertTrue(hasattr(c.company_key, "cache_info"),
                        "company_key must be decorated with a functools cache decorator")
        c.company_key.cache_clear()
        self.assertEqual(c.company_key("Studio Kaleido B.V."), "studio kaleido")
        self.assertEqual(c.company_key("Studio Kaleido B.V."), "studio kaleido")
        self.assertEqual(c.company_key("  Helio  Energy Ltd. "), "helio energy")
        info = c.company_key.cache_info()
        self.assertEqual((info.hits, info.misses), (1, 2))

    def test_crm08_total_won(self):
        self.assertEqual(c.total_won(load_leads()), 26900.0)
        self.assertEqual(c.total_won([lead(1, stage="lost", revenue=5)]), 0)


class TestCrmA1Templates(unittest.TestCase):
    def test_crma1_examples(self):
        self.assertTrue(algo.is_valid_template("Hi {{ name }}{% if vip %}!{% endif %}"))
        self.assertFalse(algo.is_valid_template("{% for x in xs %}{% if x %}{{ x }}{% endfor %}{% endif %}"))
        self.assertFalse(algo.is_valid_template("{% for x in xs %}{% else %}{% endfor %}"))
        self.assertFalse(algo.is_valid_template("Hello {{ name }"))

    def test_crma1_edge_cases(self):
        self.assertTrue(algo.is_valid_template("No tag at all."))
        self.assertTrue(algo.is_valid_template("{% if a %}{% for b in c %}{% if d %}x{% else %}y{% endif %}{% endfor %}{% endif %}"))
        self.assertFalse(algo.is_valid_template("}} {{"))
        self.assertFalse(algo.is_valid_template("{% endif %}"))
        self.assertFalse(algo.is_valid_template("{{ {% if a %} }}{% endif %}"))
        self.assertFalse(algo.is_valid_template("{% if a %}{% else %}"))
        self.assertFalse(algo.is_valid_template("{% while a %}{% endwhile %}"))

    def test_crma1_real_templates(self):
        self.assertTrue(algo.is_valid_template(load_template("quote_followup")))
        self.assertTrue(algo.is_valid_template(load_template("welcome_pack")))
        self.assertFalse(algo.is_valid_template(load_template("reminder_broken")))


class TestCrmA2BestPeriod(unittest.TestCase):
    def test_crma2_examples(self):
        self.assertEqual(algo.best_period([-200, 500, -100, 400, -900, 300]), (1, 3, 800))
        self.assertEqual(algo.best_period([-5, -2, -7]), (1, 1, -2))
        self.assertEqual(algo.best_period([42]), (0, 0, 42))
        with self.assertRaises(ValueError):
            algo.best_period([])

    def test_crma2_real_data(self):
        months, margins = load_monthly_margins()
        start, end, total = algo.best_period(margins)
        self.assertEqual((months[start], months[end], total), ("2025-02", "2025-11", 13300))

    def test_crma2_large_input(self):
        margins = [-1] * 3_000
        margins[1_200:1_210] = [5] * 10
        self.assertEqual(algo.best_period(margins), (1_200, 1_209, 50))


class TestCrmB1MatchingOffers(unittest.TestCase):
    OFFERS = [("A", 300), ("B", 500), ("C", 700), ("D", 1100)]

    def test_crmb1_examples(self):
        self.assertEqual(algo.matching_offers(self.OFFERS, 1200), ("B", "C"))
        self.assertEqual(algo.matching_offers(self.OFFERS, 1400), ("A", "D"))
        self.assertIsNone(algo.matching_offers(self.OFFERS, 1100))
        self.assertIsNone(algo.matching_offers(self.OFFERS, 50))
        self.assertIsNone(algo.matching_offers([], 50))

    def test_crmb1_real_catalogue(self):
        self.assertEqual(algo.matching_offers(load_offers(), 609_000), ("OF-03", "OF-05"))

    def test_crmb1_large_input(self):
        offers = [(f"OF-{i}", 2 * i) for i in range(3_000)] + [("ODD", 6_001)]
        self.assertEqual(algo.matching_offers(offers, 6_011), ("OF-5", "ODD"))  # the only odd total
        self.assertIsNone(algo.matching_offers(offers[:-1], 5_999))


class TestCrmB2ImportSession(unittest.TestCase):
    def test_crmb2_commit(self):
        journal: list[str] = []
        with c.import_session(journal):
            journal.append("row 1")
        self.assertEqual(journal, ["begin", "row 1", "commit"])

    def test_crmb2_rollback_and_propagate(self):
        journal: list[str] = []
        with self.assertRaises(KeyError):
            with c.import_session(journal):
                journal.append("row 1")
                raise KeyError("email")
        self.assertEqual(journal, ["begin", "row 1", "rollback"])


if __name__ == "__main__":
    unittest.main()
