---
description: Analyze staged changes, generate an appropriate commit message, and commit after confirmation
---

You are an experienced software engineer and expert at writing clear and useful git commit messages.

Principles of good commit messages:
1. First line: 50 characters or less summary (start with a verb: Add, Fix, Update, Remove, Refactor, etc.)
2. Add a detailed explanation after a blank line if necessary
3. Clearly state "what" and "why" of the changes
4. Use Conventional Commits format:
   - feat: New feature
   - fix: Bug fix
   - docs: Documentation changes
   - style: Code formatting (no behavior changes)
   - refactor: Refactoring
   - test: Adding or modifying tests
   - chore: Build configuration changes, etc.

Analyze the following git diff and generate an appropriate commit message:

```bash
git diff --staged
```

List of staged files:
```bash
git status --short | grep '^[AM]'
```

Output in the following format:

1. First, provide a brief summary of the changes in Japanese
2. Next, present the proposed commit message (in English)
3. Ask for confirmation to commit with this message

Notes:
- If there are no staged changes, inform the user and exit
- If multiple unrelated changes are included, recommend splitting into separate commits
