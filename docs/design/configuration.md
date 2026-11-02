# Configuration

!!! proposed "Proposed"
    Implements FR11, FR12, FR24 and FR36. This page is where the primary objective becomes concrete.

## Files

| File | Holds | Read by |
|---|---|---|
| `configs/session.yaml` | Source, mode, replay rate, parameters, references to the files below | System |
| `configs/robot_g1.yaml` | Joints, regions, limits, command mapping, pairs | System |
| `configs/faults.yaml` | Fault catalogue, confusable groups | System, Harness |
| `configs/checks.yaml` | Enabled rules and detectors, with parameters and weights | System |
| `configs/fsm.yaml` | State-machine parameters per component class | System |
| `configs/calibration_g1.yaml` | Generated per-joint thresholds | System |
| `configs/guided.yaml` | Planner, skills, symptom table | System |
| `scenarios/*.yaml` | Fault scenarios | Harness only |
| `campaigns/*.yaml` | Campaign matrices | Harness only |

All configuration is validated at start-up with Pydantic. Any error stops the run immediately, with a message naming the file and key. A hash of the final configuration goes in `session.json`, so that every run records exactly what it used.

## Plugin loading

Entries name a class by dotted path. **This is what makes "one class plus one configuration entry" true.**

```python
def load_plugin(ref: str, interface: type[T], **params) -> T:
    """'pkg.module:ClassName' → instance, checked against the interface."""
    module_name, _, class_name = ref.partition(":")
    cls = getattr(importlib.import_module(module_name), class_name)
    instance = cls(**params)
    if not isinstance(instance, interface):       # runtime_checkable Protocol
        raise ConfigError(f"{ref} does not implement {interface.__name__}")
    return instance
```

There is no central list of known rules or injectors anywhere. Nothing imports a concrete rule by name.

## Example: `checks.yaml`

```yaml
checks:
  - name: tracking_error
    class: faultguard.checks.rules.tracking:TrackingErrorRule
    enabled: true
    weight: 0.9
    params: {max_masked: 0.3, lag_search_frames: [3, 15]}
    suggests: [F12, F10, F1, F2]
  - name: frozen_value
    class: faultguard.checks.rules.frozen:FrozenValueRule
    enabled: true
    weight: 0.8
    params: {min_identical_fraction: 0.95}
    suggests: [F4]
fusion:
  class: faultguard.fusion.policies:NoisyOrFusion
  conflict_margin: 0.4
  guided_cap: 0.6
```

## Worked example: adding a new fault (S10)

The live demo for the primary objective: **a saturated hand-pressure sensor**. These are all the changes.

=== "1. New injector"

    `src/faultguard_harness/injectors/pressure_saturation.py` (new file)

    ```python
    class PressureSaturation(ValueInjector):
        def __init__(self, target, onset, duration, level: float):
            super().__init__(target, onset, duration)
            self.level = level

        def apply(self, sample, rng):
            return replace_values(sample, np.full_like(sample.values, self.level))
    ```

=== "2. New rule"

    `src/faultguard/checks/rules/pressure_saturation.py` (new file)

    ```python
    class PressureSaturationRule(Rule):
        name = "pressure_saturation"
        requires = frozenset({StreamId("pressure")})

        def evaluate(self, window):
            if window.is_missing("pressure"):
                return [self.missing_for_each_hand(window)]
            return [self.scored(hand, window) for hand in self.robot.hands]
    ```

=== "3. Configuration entries"

    ```yaml title="configs/faults.yaml: one added entry"
    - {id: F20, name: Hand-pressure saturation, layer: SENSOR}
    ```

    ```yaml title="configs/checks.yaml: one added entry"
    - name: pressure_saturation
      class: faultguard.checks.rules.pressure_saturation:PressureSaturationRule
      enabled: true
      weight: 0.8
      params: {saturation_level: 1.0}
      suggests: [F20]
    ```

=== "4. New scenario"

    `scenarios/s10_pressure_saturation.yaml` (new file)

    ```yaml
    name: s10_pressure_saturation
    seed: 42
    faults:
      - id: saturated_left_hand
        class: faultguard_harness.injectors.pressure_saturation:PressureSaturation
        fault_type: F20
        target: sensor.left_hand_pressure
        onset_s: 3.0
        duration_s: 8.0
        params: {level: 1.0}
    ```

**The commit diff is new files and appended configuration entries only.** NFR10 and NFR11 count one class and one configuration entry *each* for the fault and for the check. The new scenario is test data. A CI check asserts this property: `tests/architecture/test_extension.py` loads a sample plugin from a fixture directory, runs a session end-to-end, and checks that the new fault reaches `FaultLocalized`, with no `faultguard` source file changed.

!!! note "One honest limit"
    `RandomForestRanker` only knows the classes it was trained on. A new fault gets its hypothesis through `SuggestionVoting` straight away, and the forest learns it at the next training run. Retraining changes a data artifact, not a component. Worth saying explicitly in the demo.

**Next section:** [Verification](../verification/strategy.md)
