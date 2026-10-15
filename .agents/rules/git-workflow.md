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
- **Don't rewrite history** on a branch someone else is using, and never force-push `main`.
- **Large files.** GitHub warns on files over 50 MB and rejects files over 100 MB. Ask the owner before committing anything over 10 MB.
