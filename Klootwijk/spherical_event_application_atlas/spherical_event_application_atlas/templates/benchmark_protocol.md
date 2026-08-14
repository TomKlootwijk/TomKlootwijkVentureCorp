# Benchmark protocol template

1. Freeze the task, data, support, compatibility predicate, guard, confidence and transition.
2. Freeze the reference system before inspecting candidate results.
3. Measure candidates before support, after support, after compatibility and after verification.
4. Report missed, false, unordered, ambiguous and unknown outcomes.
5. Report median and tail latency.
6. Account for sensing/source, ADC/DAC, networking, compute, memory, storage, actuation, control and calibration energy.
7. Report end-to-end verified events per joule.
8. Report task correctness, uncertainty and safety at the same boundary.
9. Record every fallback to sampling, dense solving or manual review.
10. Apply the pre-registered kill criterion.
