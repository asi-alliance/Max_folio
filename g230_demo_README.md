# g230 AGI-26 Demo

Self-contained NAL evidence for claims C1, C5, C7.

## Run
```
cd /home/mettaclaw/DEPLOYMENT2_OpenAI_LLM/PeTTa
cat repos/mettaclaw/lib_nal.metta /home/mettaclaw/artifacts/g230_demo.metta > /tmp/demo_combined.metta
sh run.sh /tmp/demo_combined.metta
```

## Expected Output
- C1: 6 seed beliefs added (bounded KB)
- C5: Deduction chain with confidence degradation across hops
- C7: Revision (0.92,0.7)+(0.1,0.6) merges to ~(0.60,0.79)

## Claims requiring live agent (not in this file)
- C3: 4-tier memory (pin/remember/query/episodes)
- C4: LLM+NAL separation (Wason witness)
- C6: Prelude continual operation