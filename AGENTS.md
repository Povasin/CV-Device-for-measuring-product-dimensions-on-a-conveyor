# Ozon Tech CV Test

## Project goal

Implement a high-quality engineering solution for one selected
Computer Vision task from the Ozon Tech / Innopolis 2026 test assignment.

The final solution must satisfy every explicit requirement from the
provided test assignment.

## Priority

1. User instructions
2. Explicit requirements of the test assignment
3. AGENTS.md
4. Skills
5. Existing project conventions

Never silently violate higher-priority requirements.

## Engineering principles

- Do not implement before understanding the problem.
- Do not invent hardware specifications.
- Do not invent experimental results.
- Do not claim an algorithm works without validation.
- Prefer deterministic classical CV when it is sufficient.
- Use neural networks only when they provide a justified advantage.
- Every architectural decision must have a reason.
- Keep modules small and testable.
- Avoid unnecessary dependencies.
- Do not overengineer.

## Research

When selecting hardware, libraries or algorithms:

1. Identify the requirement.
2. Search authoritative sources.
3. Compare alternatives.
4. Record assumptions.
5. Record the source.
6. Explain the final choice.

Never use fabricated sensor specifications.

## Implementation

Before changing code:

1. Inspect the repository.
2. Understand existing interfaces.
3. Identify dependencies.
4. Write or update the relevant task.
5. Implement the smallest correct change.
6. Run tests.
7. Run lint/type checks.
8. Inspect git diff.

## Testing

Every meaningful implementation change must be validated.

At minimum:

- unit tests for core logic;
- edge cases;
- invalid input handling;
- integration test for the complete pipeline where practical.

Do not create fake tests that only reproduce the implementation.

## Documentation

Every major architectural decision must be documented.

Documentation must explain:

- problem;
- assumptions;
- chosen approach;
- alternatives;
- limitations;
- metrics;
- expected failure modes.

## Git

Use small meaningful commits.

Never commit:

- secrets;
- .env;
- generated large datasets;
- cache;
- model weights unless explicitly required;
- temporary files.

Before committing:

- run tests;
- run lint;
- inspect diff;
- verify no secrets.

## Agent behavior

Do not ask the user for confirmation for routine engineering actions.

Ask only when:
- requirements are genuinely ambiguous;
- an irreversible action is required;
- credentials are required;
- a major architectural decision changes the project direction.

Do not rewrite working code without evidence that the change improves the solution.

## Definition of Done

A task is complete only when:

- implementation is complete;
- tests pass;
- lint passes;
- documentation is updated;
- assumptions are documented;
- git diff has been reviewed.