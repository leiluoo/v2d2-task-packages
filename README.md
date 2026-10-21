# V2D2 task packages

Private dataset export of 6,878 tasks, their original input files and rubrics, available solver trajectories and deliverables, and two sets of judgments.

| Training bucket | Tasks |
| --- | ---: |
| RL | 644 |
| SFT | 933 |
| Annealing | 5,301 |

The data archives are attached to release `minimax-buckets-20261021`. The repository contains the archive manifest, task index, checksums, bucket membership and download script.

## Bucket rules

Pass rates count rubrics equally; they are not weight-adjusted scores. For three valid rollout judgments, take the union of passed rubric IDs, the mean of the three pass rates, and the mean of the two highest pass rates.

- **RL:** union >= 80%, three-rollout mean <= 60%, top-two mean <= 80%, and no RL exclusion.
- **SFT:** union >= 80% and not assigned to RL.
- **Annealing:** all remaining tasks, including incomplete or failed judgments.

RL and SFT require three complete valid judgments. Failed or missing judgments are never interpreted as zero scores. Previously identified JavaScript and other training exclusions remain effective. The 28 tasks with request-capacity/context failures are excluded from RL; all 28 are in annealing in this export.

The current bucket assignments use **MiniMax-M3.1-Flash**, with one whole-task judgment per rollout. Historical per-rubric judgments are preserved separately, including previously applied visual rejudgments. They are comparison data, not the current bucket source.

## Package layout

Each archive is independently extractable; archives contain disjoint tasks.

```text
<bucket>/tasks/<task_id>/
  task.md
  inputs/                         # Original task input files
  rubrics.json
  meta_info.json                  # Bucket, rates, exclusions and availability
  files_manifest.json             # SHA-256 for every other packaged file
  judgments/
    per_rubric_aggregate.json      # Preserved historical aggregate
  rollouts/
    rollout_01/                   # Also rollout_02 and rollout_03
      trajectory.json             # Original messages, tools and meta_info
      outputs/                    # Original solver deliverables
      judge_per_rubric.json        # Historical criterion/rubric decisions
      judge_minimax.json           # MiniMax decisions or explicit failure
      judge_minimax_record.json    # Run record, scorecard and token usage
```

When a source trajectory is absent, `trajectory_status.json` records that fact instead of inventing a trajectory. Missing artifacts are also listed in each task's metadata and the task index. Failed or missing judgments retain a null result. RL and SFT tasks have all three trajectories. Teacher model and effort are preserved in each original trajectory's `meta_info` when present in the source.

The export includes original deliverables, but excludes pre-render caches, screenshots produced for judging, and request payloads containing embedded images. Known operational credentials, if found, are redacted only in the exported copies and recorded in per-task metadata. Original source files and judgments remain unchanged.

## Download

Authenticate with GitHub CLI using an account that can access this private repository. Python 3.12 or later and `gh` are required.

```sh
python3 scripts/download.py --bucket rl --output data
python3 scripts/download.py --bucket sft --output data
python3 scripts/download.py --bucket annealing --output data
# Or download and extract all three buckets:
python3 scripts/download.py --bucket all --output data
```

The downloader verifies every archive against `manifest.json` before extraction. To download without extraction, add `--no-extract`.

`bucket_snapshot.json` contains bucket membership. `task_index.jsonl` maps each task to its archive and records trajectory availability. `task_buckets.jsonl` retains the detailed per-task bucketing audit. `SHA256SUMS` contains archive checksums.
