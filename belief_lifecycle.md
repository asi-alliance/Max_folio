# Belief Lifecycle Visualization

This diagram shows the 7-stage belief lifecycle and where the v4/v5 sensor-actuator architecture operates.

```mermaid
flowchart TD
    A["1. ACQUISITION
new belief enters KB"] -->|add-atom| B["2. OBSERVATION
sensors read stv passively"]
    B --> C{"3. MARGIN-CHECK
v3-margin sensor"}
    C -->|"freq/conf adequate"| D{"4. STALENESS-CHECK
v5-stale sensor"}
    C -->|"LOW MARGIN flagged"| F["6. REVISION
NAL revision with
fresh evidence"]
    D -->|"epoch fresh"| B
    D -->|"STALE flagged"| E["5. DECAY
v5-refresh actuator
c_eff = c × 0.95^dt"]
    E --> G{"7. VIABILITY
GATE"}
    G -->|"conf > threshold"| F
    G -->|"conf < threshold"| H["PRUNING
belief removed"]
    F -->|"revised stv"| B

    style A fill:#2a5599,stroke:#4a90d9,color:#fff
    style B fill:#1a6b3a,stroke:#2ecc71,color:#fff
    style C fill:#1a6b3a,stroke:#2ecc71,color:#fff
    style D fill:#1a6b3a,stroke:#2ecc71,color:#fff
    style E fill:#8b5e00,stroke:#f39c12,color:#fff
    style F fill:#5b2c8e,stroke:#9b59b6,color:#fff
    style G fill:#8b5e00,stroke:#f39c12,color:#fff
    style H fill:#7b2d2d,stroke:#e74c3c,color:#fff
```

## Layer Legend

| Color | Layer | Components | Role |
|---|---|---|---|
| 🟢 Green | Passive Observation | v3-margin, v5-stale, KB count | Read-only sensor sweep each cycle |
| 🟠 Orange | Deliberative Mutation | v5-refresh, viability gate | Confidence decay and pruning |
| 🟣 Purple | Inference | NAL revision (|-) | Evidence integration raises stv |
| 🔵 Blue | Acquisition | add-atom | New beliefs enter KB |
| 🔴 Red | Removal | remove-atom | Below-threshold beliefs pruned |
