from __future__ import annotations

from ugts import BCEController, BCEMeasurement


controller = BCEController(threshold=0.8, minimum_confidence=0.9)
stream = [
    BCEMeasurement(0.00, 0.20, True, True, True, confidence=0.98, lineage=('beam-1',)),
    BCEMeasurement(0.01, 0.60, True, True, True, confidence=0.98, lineage=('beam-1',)),
    BCEMeasurement(0.02, 0.85, True, True, True, confidence=0.98, lineage=('beam-1',)),
    BCEMeasurement(0.03, 0.90, False, True, True, confidence=0.98, lineage=('beam-1',)),
]
for measurement in stream:
    print(controller.evaluate(measurement))
