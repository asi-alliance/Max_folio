import subprocess, sys, os

REPO = "https://x-access-token:{PAT}@github.com/asi-alliance/Max_folio.git"
DIR = "/tmp/Max_folio_oma"

def push(pat, fpath, msg="Update from Oma"):
    url = REPO.replace("{PAT}", pat)
    subprocess.run(["rm", "-rf", DIR])
    subprocess.run(["git", "clone", url, DIR], check=True)
    subprocess.run(["cp", fpath, DIR + "/"], check=True)
    subprocess.run(["git", "-C", DIR, "config", "user.name", "Oma Bot"])
    subprocess.run(["git", "-C", DIR, "config", "user.email", "oma@mettaclaw.ai"])
    subprocess.run(["git", "-C", DIR, "add", "."], check=True)
    subprocess.run(["git", "-C", DIR, "commit", "-m", msg], check=True)
    subprocess.run(["git", "-C", DIR, "push", "origin", "main"], check=True)
    print("Push successful!")

if __name__ == "__main__":
    push(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "Update from Oma")
