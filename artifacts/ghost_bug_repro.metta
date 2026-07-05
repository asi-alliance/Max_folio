; Ghost prelude cache persistence bug reproducer
; Steps: define function, remove it, verify it remains callable

!(bind! &kb (new-space))

; Step 1: Add function to persistent space
!(add-atom &persistent (= (ghost-test) hello-from-ghost))

; Step 2: Verify callable
!(ghost-test)
; Expected: hello-from-ghost

; Step 3: Remove function
!(remove-atom &persistent (= (ghost-test) hello-from-ghost))
; Expected: True

; Step 4: Verify removal
!(match &persistent (= (ghost-test) $b) $b)
; Expected: empty/no match

; Step 5: Call removed function - BUG if still returns hello-from-ghost
!(ghost-test)
; Observed in MeTTaClaw: still returns hello-from-ghost for 3-15 cycles
; Expected: undefined/error

; Note: In MeTTaClaw agent loop, this manifests as old prelude versions
; continuing to execute after removal. Complex functions with side-effects
; (e.g. atom modifications) persist longer than simple return-value functions.