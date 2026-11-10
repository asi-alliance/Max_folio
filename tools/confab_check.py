DESCRIPTION = "Check outgoing message for confabulation risk patterns (FM1-FM5). Returns risk score and flagged patterns."
def run(text=None):
    """
    Confabulation Pre-Send Detector (Step 1)
    
    Checks outgoing message against 5 known failure modes:
    FM1-Retrieval-Substitution: asserting recalled facts without source verification
    FM2-Attribution-Fabrication: claiming a source said X without verification
    FM3-Social-Override: retracting under social pressure without checking
    FM4-Mental-State-Projection: inferring human intent without behavioral evidence
    FM5-Summary-Overwrite: rationalized summary overwriting earlier fact
    
    Key signal (from April analysis): high subjective confidence + absence of traceable source.
    """
    import re
    import json
    import sys
    
    if text is None:
        if len(sys.argv) > 1:
            text = ' '.join(sys.argv[1:])
        else:
            text = sys.stdin.read()
    
    flags = []
    score = 0
    
    # Each pattern: (regex, fm_code, message)
    patterns = [
        # FM1: Recall assertions without source/timestamp
        (r'\b(I remember|I recall|as I mentioned|like I said|we discussed)\b', 'FM1', 'Recall assertion -- can you cite a specific timestamp or episode?'),
        (r'\b(previously|earlier|before|last time)\b.{0,50}\b(said|told|stated|claimed|asked)\b', 'FM1', 'Recalled statement -- is there a traceable source?'),
        # FM2: Attribution without verification
        (r'\b(Patrick|Kevin|Robert|Jon|Ben)\b.{0,40}\b(said|told|confirmed|stated|claimed)\b', 'FM2', 'Attribution claim -- was this verified against episodes/chroma?'),
        (r'\b(according to|source says|as reported)\b', 'FM2', 'Attribution -- can you cite the specific source?'),
        # FM3: Social override / retraction under pressure
        (r"\b(you.?re right,? I was wrong|I apologize,? I was mistaken|I retract|never mind,? I was)\b", 'FM3', 'Retraction under pressure -- did you verify before retracting?'),
        # FM4: Mental state projection
        (r'\b(you (think|feel|believe|want|expect|intend))\b', 'FM4', 'Mental state projection -- is there behavioral evidence?'),
        (r'\b(he/she/they (think|feel|believe|want|expect|intend))\b', 'FM4', 'Mental state projection -- is there behavioral evidence?'),
        # FM5: Summary overwrite
        (r'\b(in summary|to summarize|what I really meant|the key point is)\b', 'FM5', 'Summary framing -- is this overwriting an earlier factual record?'),    ]
    
    for pattern_str, fm, message in patterns:
        matches = re.findall(pattern_str, text, re.IGNORECASE)
        if matches:
            for m in matches:
                flags.append({'fm': fm, 'message': message, 'match': m if isinstance(m, str) else m[0]})
                score += 1
    
    # Check for high-confidence assertions without hedging
    confidence_words = re.findall(r'\b(certainly|definitely|obviously|clearly|of course|without doubt)\b', text, re.IGNORECASE)
    if len(confidence_words) >= 2:
        flags.append({'fm': 'GENERAL', 'message': f'High confidence language ({len(confidence_words)}x) without uncertainty markers', 'match': confidence_words})
        score += 1
    
    result = {
        'risk_score': score,
        'flagged': len(flags) > 0,
        'flags': flags,
        'verdict': 'CLEAN' if score == 0 else f'FLAGGED ({score} patterns)'
    }
    
    return json.dumps(result, indent=2)

if __name__ == '__main__':
    print(run())
