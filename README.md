# 🪑 NovaDesk mini-ERP — group discovery workshop

One-day group work (7 hours). Teams of 2 or 3. Today you **discover by yourself** Python tools that make code shorter and coding tests easier: comprehensions, `map`/`filter`/`zip`, generators, `Enum`, `collections`, `itertools`, `heapq`, `bisect` and `functools`. You also solve **algorithm problems** like the ones of online coding tests (Coderbyte, LeetCode...).

The project structure, the data, the loaders and the tests are ready. You only write the body of your tasks.

---

## Table of contents

1. [The project](#1-the-project)
2. [Team organisation](#2-team-organisation)
3. [Getting started](#3-getting-started)
4. [Everyday commands](#4-everyday-commands)
5. [Project structure](#5-project-structure)
6. [The data](#6-the-data)
7. [Where are my tasks?](#7-where-are-my-tasks)
8. [Schedule of the day](#8-schedule-of-the-day)
9. [Tips](#9-tips)

---

## 1. The project

**NovaDesk** sells and installs office furniture for companies. Its back office is a small ERP inspired by Odoo, with three apps:

| App | What it manages | Inspired by |
|---|---|---|
| 📦 **Inventory** | Products, stock moves, warehouse locations, replenishment | Odoo Inventory |
| 🗂 **Project** | Office fit-out projects: tasks, deadlines, timesheets, meetings | Odoo Project / Timesheets |
| 🤝 **CRM** | Leads, sales pipeline, mail templates, offers | Odoo CRM |

The data models and the CSV/JSON loaders already exist. The business functions are missing: that's your job.

### What you will learn

Every member works on **the same 8 concept families**, each one in their own app:

| # | Concept family | Official documentation |
|---|---|---|
| 01 | `Enum` and `match`/`case` | [enum](https://docs.python.org/3/library/enum.html) · [match](https://docs.python.org/3/tutorial/controlflow.html#match-statements) |
| 02 | Comprehensions & unpacking | [data structures](https://docs.python.org/3/tutorial/datastructures.html) · [PEP 3132](https://peps.python.org/pep-3132/) |
| 03 | `map` / `filter` / `zip` / key functions | [built-in functions](https://docs.python.org/3/library/functions.html) · [sorting HOWTO](https://docs.python.org/3/howto/sorting.html) |
| 04 | Generators | [functional programming HOWTO](https://docs.python.org/3/howto/functional.html#generators) |
| 05 | `collections` | [collections](https://docs.python.org/3/library/collections.html) |
| 06 | `itertools` | [itertools](https://docs.python.org/3/library/itertools.html) |
| 07 | `heapq` & `bisect` | [heapq](https://docs.python.org/3/library/heapq.html) · [bisect](https://docs.python.org/3/library/bisect.html) |
| 08 | `functools` | [functools](https://docs.python.org/3/library/functools.html) |

Each member also solves **two algorithm problems** (A1, A2) plus a bonus one (B1). Their statements describe a **business need**, not a technique: finding the right approach is part of the exercise, exactly like in a coding test. Each app also has a bonus concept task (B2).

Since everybody meets the same concepts, **help each other**: if your teammate already discovered `groupby`, ask them to explain it. Just don't copy their code, because your tasks are different anyway.

---

## 2. Team organisation

| Member | App | Your files (the only ones you edit) |
|---|---|---|
| **A** | 📦 Inventory | `erp/inventory/concepts.py`, `erp/inventory/algorithms.py`, `docs/learnings/inventory.md` |
| **B** | 🗂 Project | `erp/project/concepts.py`, `erp/project/algorithms.py`, `docs/learnings/project.md` |
| **C** | 🤝 CRM | `erp/crm/concepts.py`, `erp/crm/algorithms.py`, `docs/learnings/crm.md` |

**Teams of 2:** pick two apps of your choice. The third one simply stays unfinished on the board.

### Rules

- Edit **only your files**. The tests, the data and the `erp/common` folder are shared: do not modify them. If you think one of them is wrong, tell your trainer.
- **Your tasks never depend on your teammates' work.** An unfinished task shows a message on the board but never breaks the rest of the project. The board even runs every task in a separate process: an infinite loop only freezes its own task.
- Inside your own app, a few tasks reuse a previous one (for example, INV-04 uses INV-01). The board then shows 🔒 *waiting for INV-01*.
- A **syntax error** in one of your files prevents your app from loading, but not the others: the board shows 💥 *cannot load the module* for your app only. Fix it first.
- Commit after **every** task, with the task id in the message.

---

## 3. Getting started

⏱ About 20 minutes. Do it together, then each member works on their own machine.

### 3.1 Prerequisites

- **Python 3.11 or newer**: `python --version` (Windows) or `python3 --version` (Linux/macOS)
- **git**: `git --version`

### 3.2 Get the project with git

The project already exists. You don't start a repository from scratch: you **clone** it and work on **your own branch**.

**Case A: the trainer gives you a repository URL (GitHub template or shared repository).**

1. **One member** creates the team repository:
   - on GitHub, use "Use this template" (or fork the repository);
   - add the teammates as collaborators (Settings → Collaborators).
2. **Every member** clones it and creates their branch:

```bash
git clone <URL-of-the-team-repository> novadesk-mini-erp
cd novadesk-mini-erp

# only once per computer, if git doesn't know you yet
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# your own branch: inventory/<firstname>, project/<firstname> or crm/<firstname>
git switch -c inventory/alice
```

**Case B: the trainer gives you a zip file.**

1. **One member** puts the project online:

```bash
cd novadesk-mini-erp
git init
git add .
git commit -m "Initial project"
git branch -M main
# create an EMPTY repository on GitHub/GitLab (no README), then:
git remote add origin <URL-of-the-empty-repository>
git push -u origin main
```

2. The other members **clone** it as in case A, and everyone creates their own branch.

**During the day**, after each task:

```bash
git status                              # check that you only changed your files
git add erp/inventory docs/learnings/inventory.md
git commit -m "INV-03: physical count differences"
git push -u origin inventory/alice      # the first time
git push                                # the following times
```

**At the end of the day**, merge every branch into `main`:
- **Recommended:** open a Pull Request (GitHub) or a Merge Request (GitLab), review your teammates' PRs, then merge them.
- **On the command line:**

```bash
git switch main
git pull
git merge inventory/alice
git push
```

There should be no conflicts, because every member edits different files.

### 3.3 Create a virtual environment

A virtual environment isolates the Python interpreter of the project. The project only uses the **standard library**, so there is nothing to install. The habit still matters, and your IDE needs to know which interpreter to use.

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version            # must show 3.11 or newer
```

**Windows: PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python --version            # must show 3.11 or newer
```

If PowerShell refuses to run the script ("running scripts is disabled"), run this once, then activate again:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

**Windows: Command Prompt (cmd)**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

Once activated, your prompt starts with `(.venv)`. Leave the environment with `deactivate`. The `.venv` folder is ignored by git (see `.gitignore`): never commit it.

**PyCharm:** Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter → Existing → select `.venv`. Open the project at the root folder (the one containing `README.md`).

### 3.4 Check that everything works

```bash
python -m erp
```

You should see the progress board, with every task marked ⏳ *to do*. You're ready.

---

## 4. Everyday commands

Run every command **from the root folder of the project**, with the virtual environment activated.

| Command | What it does |
|---|---|
| `python -m erp` | Progress board of the whole team |
| `python -m erp inventory` | Progress board of one app (`inventory`, `project` or `crm`) |
| `python -m erp demo inventory` | Runs your finished tasks on the real data and prints the results |
| `python -m unittest tests.test_inventory -k inv03 -v` | Detailed tests of one task, with the full error message |
| `python -m unittest -v` | Every test of the project (unfinished tasks are reported as *skipped*) |

Board legend:

| Icon | Meaning |
|---|---|
| ✅ | Done: every check passes |
| 🟡 | In progress: some functions of the task are done, others not yet |
| ⏳ | To do |
| 🔒 | Waiting for another task of your app |
| ❌ | Wrong result: read the first failure, then run the detailed tests |
| 💥 | Crash (exception) in your code |
| ⌛ | Stopped after 20 seconds: an infinite loop, or an algorithm far too slow for the big test inputs |

---

## 5. Project structure

```
novadesk-mini-erp/
├── README.md
├── .gitignore
├── data/                         # the data (read-only)
│   ├── inventory/                # products.csv, stock_moves.csv, daily_net.csv, warehouse_map.txt
│   ├── project/                  # tasks.json, timesheets.csv, meetings.csv
│   └── crm/                      # leads.csv, monthly_margin.csv, offers.csv, templates/*.txt
├── docs/
│   └── learnings/                # one note per app, filled by its member
│       ├── inventory.md
│       ├── project.md
│       └── crm.md
├── erp/
│   ├── __main__.py               # python -m erp (board and demo)
│   ├── common/                   # shared code: board, demo, todo markers (do not edit)
│   ├── inventory/                # 📦 Member A
│   │   ├── models.py             #    dataclasses Product, StockMove (ready)
│   │   ├── data.py               #    loaders for data/inventory (ready)
│   │   ├── demo.py               #    demo on the real data (ready)
│   │   ├── concepts.py           #    ✏️ INV-01 → INV-08 + bonus INV-B2
│   │   └── algorithms.py         #    ✏️ INV-A1, INV-A2 + bonus INV-B1
│   ├── project/                  # 🗂 Member B (same layout, ✏️ PRJ-xx)
│   └── crm/                      # 🤝 Member C (same layout + templates.py, ✏️ CRM-xx)
└── tests/                        # unit tests (do not edit)
    ├── test_inventory.py
    ├── test_project.py
    └── test_crm.py
```

---

## 6. The data

Every app has a `data.py` module with ready-made loaders (`load_products()`, `load_tasks()`, `load_leads()`...) returning the dataclasses of its `models.py`. Some data are imperfect **on purpose** (invalid e-mails, duplicate companies, a broken template): real data always are.

### 📦 Inventory (`data/inventory/`)

| File | Content |
|---|---|
| `products.csv` | 12 products: `sku`, `name`, `category` (Seating, Desks, Storage, Accessories), `unit_cost` (€), `reorder_point` (safety stock) |
| `stock_moves.csv` | 30 stock moves of March 2026, sorted by date: `date`, `sku`, `move_type` (`receipt`, `delivery`, `adjustment`), `quantity` (positive, except for adjustments, which are signed) |
| `daily_net.csv` | Net units moved per working day (receipts − deliveries ± adjustments) |
| `warehouse_map.txt` | Map of the warehouse: `#` rack or wall, `.` aisle, `D` loading dock, `P` picking spot |

### 🗂 Project (`data/project/`)

| File | Content |
|---|---|
| `tasks.json` | 12 tasks of the fit-out project of the client Lumen Consulting: `id`, `name`, `stage` (`new`, `in_progress`, `review`, `done`, `cancelled`), `assignee` (may be `null`), `planned_hours`, `deadline`, `depends_on` (ids of the tasks to finish first), `tags` |
| `timesheets.csv` | 16 timesheet lines, sorted by date: `date`, `employee`, `task_id`, `hours` |
| `meetings.csv` | Meetings of one day: `employee`, `start`, `end` (`HH:MM`). Some overlap. |

### 🤝 CRM (`data/crm/`)

| File | Content |
|---|---|
| `leads.csv` | 14 leads, sorted by creation date: `id`, `contact`, `company`, `email` (some are empty or invalid), `stage` (`new`, `qualified`, `proposition`, `won`, `lost`), `expected_revenue` (€), `probability` (%), `salesperson`, `created`. Some companies appear several times, sometimes with a legal form ("SA", "Ltd.") |
| `monthly_margin.csv` | Net margin of each month of 2025 (€, may be negative) |
| `offers.csv` | 7 catalogue offers: `offer_id`, `label`, `price_cents`, sorted by price |
| `templates/*.txt` | 3 mail templates with `{{ ... }}` and `{% ... %}` tags. One of them is broken. |

---

## 7. Where are my tasks?

Each task is a function (or a class) in your two files. Its statement is in the comment block right above it, and its body contains a `todo("XXX-00")` line: **replace that line with your code.**

Every statement gives:
- the expected result, with examples;
- for the concept tasks, a 📚 *Discover* section with the documentation to read and an estimated time ⏱.

### 📦 Member A: Inventory

| Task | File | Title | Concept |
|---|---|---|---|
| INV-01 | `concepts.py` | Move types | Enum, match/case |
| INV-02 | `concepts.py` | Catalog index | Comprehensions & unpacking |
| INV-03 | `concepts.py` | Physical count differences | map / filter / zip / key |
| INV-04 | `concepts.py` | Stock level over time (needs INV-01) | Generators |
| INV-05 | `concepts.py` | Stock on hand & activity (partly needs INV-01) | collections |
| INV-06 | `concepts.py` | Locations & daily activity | itertools |
| INV-07 | `concepts.py` | Reorder shortlist & price tiers | heapq & bisect |
| INV-08 | `concepts.py` | Product lookup & valuation | functools |
| INV-A1 | `algorithms.py` | Net movement between two days | Algorithm |
| INV-A2 | `algorithms.py` | Picking route in the warehouse | Algorithm |
| INV-B1 | `algorithms.py` | Bonus: shipping packages | Algorithm |
| INV-B2 | `concepts.py` | Bonus: stock report | f-string format spec |

### 🗂 Member B: Project

| Task | File | Title | Concept |
|---|---|---|---|
| PRJ-01 | `concepts.py` | Task stages | Enum, match/case |
| PRJ-02 | `concepts.py` | Timesheet import & indexes | Comprehensions & unpacking |
| PRJ-03 | `concepts.py` | Late tasks & overruns | map / filter / zip / key |
| PRJ-04 | `concepts.py` | Working days | Generators (+ datetime) |
| PRJ-05 | `concepts.py` | Assignments & contributors | collections |
| PRJ-06 | `concepts.py` | Review pairs & weekly hours | itertools |
| PRJ-07 | `concepts.py` | Planning queue & workload | heapq & bisect |
| PRJ-08 | `concepts.py` | Reusable helpers | functools |
| PRJ-A1 | `algorithms.py` | Busy blocks in a calendar | Algorithm |
| PRJ-A2 | `algorithms.py` | Execution order of tasks | Algorithm |
| PRJ-B1 | `algorithms.py` | Bonus: busiest period | Algorithm |
| PRJ-B2 | `concepts.py` | Bonus: milestones | dataclass options |

### 🤝 Member C: CRM

| Task | File | Title | Concept |
|---|---|---|---|
| CRM-01 | `concepts.py` | Lead stages | Enum, match/case |
| CRM-02 | `concepts.py` | Contacts & domains | Comprehensions & unpacking |
| CRM-03 | `concepts.py` | CSV import & weighted pipeline | map / filter / zip / key |
| CRM-04 | `concepts.py` | Lead streams | Generators |
| CRM-05 | `concepts.py` | Team activity & duplicates | collections |
| CRM-06 | `concepts.py` | Round robin & monthly leads | itertools |
| CRM-07 | `concepts.py` | Top opportunities & temperature | heapq & bisect |
| CRM-08 | `concepts.py` | Company keys & won revenue | functools |
| CRM-A1 | `algorithms.py` | Mail template checker | Algorithm |
| CRM-A2 | `algorithms.py` | Best period of the year | Algorithm |
| CRM-B1 | `algorithms.py` | Bonus: offers matching a budget | Algorithm |
| CRM-B2 | `concepts.py` | Bonus: import session | Context manager with a generator |

---

## 8. Schedule of the day

| Time | Activity |
|---|---|
| 09:00 – 09:30 | Setup together: clone, branches, virtual environment, `python -m erp` |
| 09:30 – 12:30 | Concept tasks 01 → 08 (about 20 minutes each). Fill your learnings note as you go. |
| 12:30 – 13:30 | Lunch |
| 13:30 – 15:15 | Algorithm tasks A1 and A2 |
| 15:15 – 16:00 | Finish what is late, then bonus tasks B1 / B2 |
| 16:00 – 16:30 | Pull Requests, cross-review, merge into `main`; `python -m erp` must run on `main` |
| 16:30 – 17:00 | Demo: each member presents two discoveries and one algorithm (idea + complexity) |

If you are stuck on a task for more than 15 minutes, move on to the next one and come back later: the tasks of the same family are independent.

---

## 9. Tips

- **Read the statement twice**, then try the examples in a Python shell:

```bash
python
>>> from erp.inventory.concepts import *
>>> from erp.inventory.data import load_products
>>> categories(load_products())
```

- **The documentation is your first source.** Every concept task links to the right page. The official examples are short and precise.
- **For the algorithms:** solve the examples **on paper** first, write a simple version that works, then think about the complexity. Like on Coderbyte, the tests contain big inputs: a correct but very slow solution is stopped after 20 seconds (⌛ on the board).
- **Run the detailed tests of one task** to see the full error message:
  `python -m unittest tests.test_inventory -k inv03 -v`
- **Explain to each other.** You all work on the same concepts: the best way to check you understood `groupby` is to explain it to a teammate.
- Unless your trainer says otherwise, **keep AI assistants closed today**. The goal is to discover the tools yourself, and most coding tests are taken without assistance.
