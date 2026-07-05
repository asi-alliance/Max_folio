import subprocess
import sys
from collections import defaultdict

def get_atoms():
    result = subprocess.run(['metta'], input='(get-atoms &persistent)', capture_output=True, text=True)
    return result.stdout

def enumerate_pairs():
    result = subprocess.run(['metta'], input='(collapse (match &persistent ((--> $A $B) (stv $F $C)) (list $A $B)))', capture_output=True, text=True)
    return result.stdout

def find_clusters(pairs_output):
    pred_to_subjects = defaultdict(set)
    for line in pairs_output.strip().split('\n'):
        line = line.strip().strip('()')
        if 'list' in line:
            parts = line.replace('list', '').strip().strip('()').split()
            if len(parts) == 2:
                subj, pred = parts[0], parts[1]
                pred_to_subjects[pred].add(subj)
    clusters = []
    for pred, subjects in pred_to_subjects.items():
        if len(subjects) >= 2:
            clusters.append((pred, list(subjects)))
    return clusters

def mint_concept(clusters, concept_name=None, tv_f=0.9, tv_c=0.9):
    bang_lines = []
    for pred, subjects in clusters:
        if not concept_name:
            concept_name = f"cluster_{pred}"
        bang_lines.append(f'!(add-atom &persistent ({concept_name}))')
        for subj in subjects:
            bang_lines.append(f'!(add-atom &persistent ((--> {subj} {concept_name}) (stv {tv_f} {tv_c})))')
    return '\n'.join(bang_lines)

if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) > 1 else 'generate'
    if action == 'generate':
        pairs = enumerate_pairs()
        clusters = find_clusters(pairs)
        for c in clusters:
            print(f"Cluster: {c[0]} -> {c[1]}")
        output = mint_concept(clusters)
        print(f"\nGenerated bang expressions:\n{output}")
        with open('/tmp/mint_novel.metta', 'w') as f:
            f.write(output + '\n')
        print(f"\nWritten to /tmp/mint_novel.metta")