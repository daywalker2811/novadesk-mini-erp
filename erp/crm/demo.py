"""Demo of the CRM tasks on the real data (python -m erp demo crm)."""

from erp.common.todo import require_enum
from erp.crm import algorithms as algo
from erp.crm import concepts as c
from erp.crm.data import load_lead_rows, load_leads, load_monthly_margins, load_offers, load_template, template_names


def _best_period() -> str:
    months, margins = load_monthly_margins()
    start, end, total = algo.best_period(margins)
    return f"{months[start]} → {months[end]}: {total} €"


def _session_journal() -> list[str]:
    journal: list[str] = []
    with c.import_session(journal):
        journal.append("14 leads imported")
    return journal


def steps():
    leads = load_leads()
    headers, rows = load_lead_rows()
    return [
        ("CRM-01", "default probabilities",
         lambda: require_enum(c.LeadStage, "CRM-01") or {s.value: s.default_probability for s in c.LeadStage}),
        ("CRM-02", "contact of lead 1", lambda: c.split_contact_name(leads[0].contact)),
        ("CRM-02", "e-mail domains", lambda: sorted(c.email_domains(leads))),
        ("CRM-03", "first CSV row as dict", lambda: c.row_to_dict(headers, rows[0])),
        ("CRM-03", "weighted pipeline", lambda: c.weighted_pipeline(leads)),
        ("CRM-04", "leads with a valid e-mail", lambda: [lead.id for lead in c.valid_leads(leads)]),
        ("CRM-05", "leads per salesperson", lambda: c.leads_per_salesperson(leads)),
        ("CRM-05", "same company, several leads", lambda: c.companies_with_multiple_leads(leads)),
        ("CRM-06", "round robin on the March leads", lambda: c.assign_round_robin([l.id for l in leads if l.created.month == 3], ["lea", "karim", "sophie"])),
        ("CRM-06", "leads per month", lambda: c.leads_per_month(leads)),
        ("CRM-07", "top 3 opportunities", lambda: c.top_opportunities(leads, 3)),
        ("CRM-07", "temperatures", lambda: [c.temperature(score) for score in (15, 40, 69, 70, 95)]),
        ("CRM-08", "company keys", lambda: sorted({c.company_key(lead.company) for lead in leads})),
        ("CRM-08", "won revenue", lambda: c.total_won(leads)),
        ("CRM-A1", "templates", lambda: {name: algo.is_valid_template(load_template(name)) for name in template_names()}),
        ("CRM-A2", "best period of 2025", _best_period),
        ("CRM-B1", "offers for a 6,090 € budget", lambda: algo.matching_offers(load_offers(), 609_000)),
        ("CRM-B2", "import session", _session_journal),
    ]
