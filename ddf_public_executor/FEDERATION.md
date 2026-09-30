# Zero-Cost Federated DDF Compute Fabric

Public generic executor only. No certified asset, proprietary oracle, private vector, production host or secret is present.

Armed providers:
- GitHub Actions: active, 20 concurrent public runners, 4 vCPU each.
- CircleCI: configuration ready, 30-way free plan target.
- Cirrus CI: configuration ready, 128-task OSS matrix target.
- Travis CI: configuration ready, 20-way free-plan target.
- Buildkite: configuration ready, 10 hosted jobs / 20 vCPU free-plan target.

Logical namespace remains 4,194,304 lanes. Physical workers are counted only after real execution evidence exists.

Determinism rules:
- immutable candidate ID;
- exclusive candidate ownership;
- no duplicate promotion;
- per-result SHA-256 evidence;
- no access to certification infrastructure;
- no paid fallback;
- no account/quota circumvention.
