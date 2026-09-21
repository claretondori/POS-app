#  Enterprise Point of Sale (POS) Architecture

A production-grade, highly scalable, asynchronous Point of Sale (POS) backend engine engineered utilizing the Clean Architecture pattern, driven by FastAPI, SQLAlchemy, and PostgreSQL.

---

##  Core Technologies
*   **Framework:** FastAPI (Asynchronous Python Web Framework)
*   **Database Engine:** PostgreSQL
*   **ORM / Data Layer:** SQLAlchemy (Asyncio Model)
*   **Data Validation:** Pydantic V2

---

##  System Domain & Business Logic

This repository houses a high-throughput **asynchronous Point of Sale (POS) backend core** designed to serve as the unified system of record for retail, wholesale, and inventory operations. It handles real-time retail commerce processing, ledger maintenance, and supply-chain logistics tracking through structured database transactions.

###  Core System Responsibilities (What It Does)

*   **Transactional Lifecycle Engine (`Sale` & `SaleItem`):** Automates point-of-sale checkout workflows. It dynamically calculates multi-item line totals, aggregates taxes, applies product-specific pricing formulas, and automatically updates business logic across child ledgers upon ticket completion.
*   **Inventory Velocity & Tracking (`Product` & `Category`):** Real-time inventory tracking engine. It acts as the gatekeeper for stock levels, preventing product updates that violate business invariants (e.g., negative stock thresholds), mapping item margins, and grouping asset portfolios under strict categorization structures.
*   **Dual-Sided CRM Ledger (`Customer` & `Supplier`):** Maintains independent balance states for accounts payable and receivable. It tracks vendor wholesale procurement histories alongside historical client sales pipelines, enabling complex operational logic like wholesale lines of credit and customer loyalty tracking.
*   **Audit-Safe Financial Close (`Payment` & `Receipt`):** Implements absolute database state guardrails for payment processing. It verifies multi-method split payments (Cash, Card, Digital Ledger) against open ticket values before auto-generating cryptographically traceable receipt hashes to protect against system drift and transaction loss.
*   **RBAC Identity Framework (`User` & `Auth`):** Enforces a rigid Role-Based Access Control (RBAC) schema via OAuth2 JWT workflows, binding incoming requests to specific terminal permissions (e.g., Cashier vs. Inventory Manager vs. Corporate Auditor).

---

##  Architectural Topology

This system strictly enforces **Clean Architecture** and **Domain-Driven Design (DDD)** constraints. By cleanly separating the system into boundaries, business rules remain infrastructure-agnostic, decoupled from databases, frameworks, and external clients.

```text
pos/app/
├── core/             # Framework-independent configurations, security primitives
├── models/           # Infrastructure Layer: Declarative SQLAlchemy Database Entities
├── schemas/          # Application Boundary Layer: Pydantic Validation & DTO Models
├── repositories/     # Data Access Layer: Generic Encapsulation of DB CRUD Operations
├── services/         # Application Business Layer: Core Process Workflow & Business Invariants
├── routers/          # Presentation Layer: FastAPI Routing & Request/Response Lifecycle
├── tests/            # Automated Test Suite (PyTest framework implementation)
├── main.py           # Application Bootstrap Engine
├── database.py       # Asynchronous Session and Database Connection Lifecycle Manager
└── dependencies.py   # Global Inversion of Control (IoC) Dependency Injection Declarations
```

---

##  Technical Capabilities

*   **Layered Decoupling:** Complete isolation of Concerns. `Services` control transaction workflows; `Repositories` isolate SQL semantics; `Routers` handle HTTP bindings.
*   **Asynchronous Processing Flow:** Fully native async database sessions managed through SQLAlchemy's `asyncio` execution model to handle concurrent throughput under load.
*   **Structured Schemas & Guardrails:** Strict payload validation, serialization formatting, and clear API boundaries implemented via custom Pydantic V2 DTOs (`schemas/`).
*   **Comprehensive Relational Mapping:** Complex system database design mapping many-to-many relationships (Sales ↔ Products via Sale Items), tracking payment transitions, audit trails, and customer metrics.
*   **Automated Verification:** Test workflows driven via `pytest` leveraging `conftest.py` configurations to construct fresh virtual test data structures per test lifecycle pass.

---

##  Domain Model Schema Matrix

The application coordinates an interconnected matrix of transactional enterprise modules:

| Sub-Domain Layer | Core Model Bound | Responsibility | Dependencies |
| :--- | :--- | :--- | :--- |
| **Identity Access** | `User` | Credential security, role scopes, auth token provisioning | — |
| **CRM Matrix** | `Customer`, `Supplier` | Customer profiling, vendor ledgers, balance histories | — |
| **Inventory Ledger** | `Product`, `Category` | Stock velocity tracking, cost pricing matrices, catalog rules | `Category` |
| **Transaction Core** | `Sale`, `SaleItem` | Aggregation workflows, dynamic transaction line calculation | `User`, `Customer`, `Product` |
| **Financial Ledger** | `Payment`, `Receipt` | Multi-method transaction resolution, audit tracking keys | `Sale` |

---

##  Engineering & Initialization Sequence

### Prerequisite Dependencies
*   **Python Engine:** `v3.11+`
*   **Database Engine:** `PostgreSQL 15+` (or alternative target relational DB)

### 1. Environment Topology Setup
Clone the application layout to your workstation and establish your virtual execution runtime environment:
```bash
git clone https://github.com
cd pos-architecture-engine

# Initialize virtual runtime container
python3 -m venv env
source env/bin/activate
```

### 2. Dependency Resolution
Compile and bind the core infrastructure dependencies directly into your application space:
```bash
pip install --upgrade pip
pip install -r pos/app/requirements.txt
```

### 3. Application Execution Boundary
Spin up the development orchestration gateway server with auto-reload monitors attached:
```bash
uvicorn pos.app.main:app --host 0.0.0.0 --port 8000 --reload
```
*   **Interactive Context Interface Docs (Swagger UI):** `http://localhost:8000/docs`
*   **Alternative Schema Specification Docs (ReDoc):** `http://localhost:8000/redoc`

---

##  Testing Strategy & Execution Boundary

The testing strategy uses clean runtime isolation. Unit, architectural binding, and transactional integration regression passes are handled through `pytest`. 

To launch the automation validation cycle, execute:
```bash
pytest pos/app/tests/ -vv --disable-warnings
```

---

##  Scalability Roadmap Targets
*   **Distributed Cache Boundary:** Introduce a Redis layer within `repositories/base.py` to cache index payloads (Product Catalogs, Categories).
*   **Database Migrations Integration:** Integrate Alembic migration streams for multi-environment production database schema drift execution.
*   **Containerized Portability Structure:** Package application bounds within Multi-Stage build configurations via Docker Compose.
