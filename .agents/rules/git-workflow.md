# Rule: git workflow

- **Never push to `main`.** The owner reviews and merges every change. Decision D-6 is still open; this is the default until it's decided.
- **One branch per topic,** named `<role>/<topic>`. Examples:
  - `docs/cp-01-tp-markdown` for document control
  - `architect/tp-01-rev-c` for the architect
  - `agents/<topic>` for changes to `.agents/` itself
- **One topic per pull request.** Keep the diff small enough to review in one sitting, with one commit per logical step.
- **Commit subjects** are short and imperative, with a scope prefix. Examples: `docs: convert TP-KRC3006-01 to Markdown`, `agents: add doc-audit skill`.
- **The pull request description** has these parts:
  - a summary
  - the files changed
  - the checks you ran, with their results
  - what you didn't verify
  - decisions needed from the owner
  - questions for other roles
- **Binary files need a reviewable companion.** `.gitattributes` marks `.ods`, `.odt`, `.pdf`, `.sr` and images as binary. Put a PDF render, a text redline or a screenshot in the pull request alongside any binary change.
- **Logs are reviewed as cell diffs.** Flat ODF logs (`.fods`) are text, but their raw diffs are flooded by LibreOffice's style renumbering ([documents.md](documents.md)).
  - Run this once in each clone, so `git diff` and `git log -p` show changed cells instead of raw XML:

    ```sh
    git config diff.odscells.textconv "python3 .agents/skills/read-odf/scripts/ods_cells.py"
    ```

  - `.gitattributes` already routes `*.fods` through this driver. Without the setting, git falls back to the raw diff.
  - GitHub's web view always shows the raw diff, so paste the cell diff (`git diff main -- '*.fods'`) into the pull request.
- **Don't rewrite history** on a branch someone else is using, and never force-push `main`.
- **Large files.** GitHub warns on files over 50 MB and rejects files over 100 MB. Ask the owner before committing anything over 10 MB.
