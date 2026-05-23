# FCCD DES Orchestration Skill Card v1.0
## Agent-Side FCCD Audit Event Processing Loop
### 7-Step Pattern (mirrors DES prototype proven in g449)
1. MATCH: metta (match &persistent ((--> audit_task $id) (stv $f $c)) $id)
2. SELECT: Agent picks min-cycle AuditTask
3. REMOVE: metta (remove-atom &persistent ((--> audit_task $id) (stv $f $c)))
4. EXTRACT: Read context_pair, theta, cycle from AuditTask atom properties
5. INVOKE: shell python3 /home/mettaclaw/artifacts/fccd_des_integration.py --audit $id
6. WRITE-BACK: If COLLISION add quarantine_registered + re_audit_scheduled atoms. If CLEAN add audit_clean atom.
7. CHAIN: Run metta (fc-step5-novel-via audit_task) on new atoms
### Key Differences from DES Prototype
- FCCD events require Python invocation (FCCDEngine) not pure MeTTa
- Theta expands per Ben Theorem 5: next_theta = theta + theta_gap * 0.1
- Q_COMPARTMENTALIZED quarantine gates belief admission until resolution
- AuditTask atoms carry theta across cycles
### Validated Components
- fccd_v01.py: FCCDEngine with scheduled_audit
- quarantine_tracker_v07.py: Q_COMPARTMENTALIZED + fair_select
- cert_layer_v07.py: certification with collision_gap
- fccd_quarantine_cert_pipeline.py: COLLISION→quarantine→cert→admit
- fccd_des_integration.py: DES event scheduling + process_audit_event
### Atom Schemas
- AuditTask id context_pair theta cycle
- CollisionToken collision_id theta_gap context_pair
- ((--> audit_task work_social_honesty_1) (stv 0.286 0.9))
- ((--> cycle work_social_honesty_1) (stv 1 0.9))
### 120-Atom FIFO Constraint
Only seed active context pairs. Selective seeding required.