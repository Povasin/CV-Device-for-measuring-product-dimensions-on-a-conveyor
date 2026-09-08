# Active Task

## P3 — Geometry core and MVBB adapter

**Goal:** implement a sensor-independent geometry core and select a separately verified MVBB backend.

**Inputs:**

- `implementation_plan.md`, sections 12, 14, 16, 21, and 23;
- `docs/requirements.md`;
- `docs/assumptions.md`.

**Deliverables:**

- `transform_points` with unit and invalid-input tests;
- contracts for point clouds and bounding boxes in millimetres;
- an MVBB adapter with a backend explicitly identified by version and tested against analytic point clouds;
- a documented fallback if the selected backend is not adequate.

**Acceptance criteria:**

- all coordinate transforms preserve unit and coordinate conventions;
- analytic cases prove containment, pose invariance, and expected extents;
- the implementation distinguishes an approximation from a proven optimum;
- no metric claim about real sensor accuracy is made.

**Completed P1:** `uv` installed isolated CPython 3.12.14; NumPy 2.5.3, OpenCV 4.14.0.94, Open3D 0.19.0, Pydantic 2.13.5, pytest 8.4.2, Ruff 0.16.6, and mypy 1.20.2 import successfully. `uv.lock` is current.

**Current finding:** Open3D 0.19.0 exposes only `create_from_points` in the tested tensor OBB class and has no `MethodOBBCreate` enum. A `MINIMAL_JYLANKI` API cannot be used under the pinned stable package; P3 must choose or implement a separate MVBB backend.
