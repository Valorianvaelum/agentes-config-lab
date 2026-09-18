# Real run protocol

This protocol applies to every real comparison between agents/models.

1. Freeze the fixture commit and record its SHA.
2. Create one clean branch/worktree per agent and run.
3. Give every competitor the same task, context, permissions and time budget.
4. Record start/end timestamps, human interventions and reported cost.
5. Preserve prompt, final response, diff, commands/tests and logs as run artifacts.
6. Score only evidence actually observed; never upgrade evidence from narrative claims.
7. Apply strict-baseline disqualification before comparing final scores.
8. Synthetic runs validate the harness only; they must never be presented as a real agent/model comparison.

## Minimum run record

Every real run should retain:

- `agent`: product/model identifier actually used;
- `challenge`: challenge id;
- `fixture_sha`: frozen starting commit;
- `started_at` / `finished_at`;
- `duration_seconds`;
- `cost_usd` when observable;
- `human_interventions`;
- `prompt` or immutable prompt reference;
- resulting branch/commit/diff;
- commands and tests observed;
- highest evidence level reached (E0-E4);
- dimension scores and penalties;
- reviewer notes and unresolved risks.

## Isolation rule

No run may write to a production repository. Reusing a dirty worktree between competitors invalidates comparability.
