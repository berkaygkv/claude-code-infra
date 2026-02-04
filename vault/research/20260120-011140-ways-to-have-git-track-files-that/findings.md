---
type: research-output
id: OUTPUT-20260120-011140-ways-to-have-git-track-files-that
target-id: TARGET-20260119-220941
status: draft
created: 2026-01-20
researcher: claude-deep-research
confidence: medium
---

# Research Output: ways to have git track files that physically live in a different directory than

**Target:** [[research/targets/TARGET-20260119-220941-the-key-features-of-uv-package-manager]]

**Question:** Research ways to have git track files that physically live in a different directory than the repository.

Context: We have:
- Git repo at `/home/user/Dev/kh/` 
- Obsidian vault at `/home/user/Dev/Docs...

---

## Findings

Perfect. Now I have comprehensive information. Let me compile this research into a well-structured output.

Based on my thorough investigation across multiple sources and approaches, I've identified several methods to have Git track files that physically live outside the repository directory. Here's what I found:

## Research Summary

### Question/Topic
How can Git track files that physically live in a different directory than the repository, specifically for tracking notes that physically reside in an Obsidian vault (`/home/user/Dev/Docs/.obs-vault/`) while being version-controlled by a separate Git repository (`/home/user/Dev/kh/`)?

### Key Findings

1. **Git cannot natively track files outside its repository boundary** - Git repositories are fundamentally designed to track only files within the directory containing the `.git` folder and its subdirectories.

2. **The bare repository approach with `--git-dir` and `--work-tree` is the only true solution** - This is the exact pattern used successfully for dotfiles management and allows tracking files in one location with the Git metadata stored elsewhere.

3. **Symlinks are your current approach and are properly tracked** - Git tracks symlinks themselves (not their targets), which is why your current setup doesn't work as desired.

4. **Bind mounts are transparent to Git but don't persist** - While bind mounts would make files appear in the repo directory, they're filesystem-level operations that don't persist in the repository.

### Detailed Analysis

#### Option 1: Bare Repository with `--git-dir` and `--work-tree` (RECOMMENDED)

This is the **only true solution** that allows files to physically live in one location while being tracked by a repository stored elsewhere.

**How it works:**
- Store the Git metadata (`.git` directory) in the `kh` repository location
- Set the work tree to point to the Obsidian vault location
- Use Git's `--git-dir` and `--work-tree` flags to operate on files

**Setup process:**

```bash
# Initialize a bare repository in your kh directory
cd /home/user/Dev/kh/
git init --bare .git-notes

# Create an alias for convenience
alias kh-notes='git --git-dir=/home/user/Dev/kh/.git-notes --work-tree=/home/user/Dev/Docs/.obs-vault/kh/notes'

# Configure to hide untracked Obsidian files
kh-notes config --local status.showUntrackedFiles no

# Now you can track specific files
kh-notes add /home/user/Dev/Docs/.obs-vault/kh/notes/overview.md
kh-notes commit -m "Track overview"
kh-notes status
```

**Advantages:**
- Files physically live in Obsidian vault (proper indexing)
- Git tracks them from your kh repository
- No symlinks needed
- Full Git functionality available
- Well-established pattern (used widely for dotfiles)

**Disadvantages:**
- Requires using custom alias or specifying flags every time
- More complex mental model than standard Git
- Team members need to understand the setup
- Some Git tools/IDEs may not handle this configuration

**Production considerations:**
- Add the alias to your shell configuration (`~/.bashrc`, `~/.zshrc`)
- Document this setup clearly for future reference
- Consider creating helper scripts for common operations
- The `.git-notes` bare repository should be backed up separately

#### Option 2: Git Worktrees (NOT SUITABLE)

**What it is:** Git worktrees allow checking out multiple branches simultaneously in different directories from the same repository.

**Why it doesn't solve your problem:**
- Worktrees are still tied to the repository boundary
- They're designed for parallel branch work, not external directory tracking
- The worktree directories must contain repository content, not arbitrary external files

**Verdict:** Not applicable to your use case.

#### Option 3: Git Submodules (NOT SUITABLE)

**What it is:** Submodules allow embedding one Git repository inside another as a tracked reference.

**Why it doesn't solve your problem:**
- Requires the Obsidian vault itself to be a Git repository
- Creates a repository-within-repository structure
- You'd be tracking the submodule reference, not the actual files
- The vault would need its own `.git` directory

**Verdict:** Architecturally wrong for this scenario.

#### Option 4: Git Subtrees (NOT SUITABLE)

**What it is:** Subtrees copy external repository content into a subdirectory and merge the history.

**Why it doesn't solve your problem:**
- Still requires files to be physically inside your repository
- Merges external history into your repo
- Doesn't allow files to live externally

**Verdict:** Doesn't meet the physical location requirement.

#### Option 5: Symbolic Links (YOUR CURRENT APPROACH - LIMITED)

**How Git handles symlinks:**
Git tracks the symlink itself (the path it points to), not the target file contents. When you commit a symlink, Git stores a blob containing the link path.

**Critical gotcha:**
Use **relative paths**, not absolute paths, for portability:
```bash
# Wrong (machine-specific):
ln -s /home/user/Dev/Docs/.obs-vault/kh/notes ./notes

# Correct (portable):
cd /home/user/Dev/kh/
ln -s ../../../Docs/.obs-vault/kh/notes notes
```

**Why this doesn't solve your problem:**
- Files still physically live in the kh repository location
- Obsidian would need to work through the symlink (indexes the kh location, not the vault)
- You want the opposite: files in vault, tracked by kh repo

**Verdict:** Not suitable for your requirements.

#### Option 6: Linux Bind Mounts (NOT PERSISTENT)

**What it is:** Filesystem-level operation that makes one directory appear in another location.

```bash
# Mount vault notes into kh repo
sudo mount --bind /home/user/Dev/Docs/.obs-vault/kh/notes /home/user/Dev/kh/notes
```

**How Git handles it:**
Git sees bind mounts transparently - it treats files at the mount point as regular files and tracks them normally.

**Why it doesn't solve your problem:**
- Bind mounts don't persist across reboots
- Must be recreated manually or via `/etc/fstab`
- Not portable to other machines
- Git doesn't store the mount information
- When someone clones your repo, they get an empty `notes/` directory

**Verdict:** Not suitable for version-controlled projects.

#### Option 7: Sparse Checkout (NOT APPLICABLE)

**What it is:** A Git feature to check out only specific subdirectories from a repository.

**Why it doesn't solve your problem:**
- Only works with directories **already inside** the repository
- Cannot reference external directories
- Designed for reducing working tree size, not extending it

**Verdict:** Not applicable to tracking external directories.

### Limitations & Gotchas

**Bare repository approach:**
- The `--git-dir` and `--work-tree` flags don't expand tilde (`~`). Use `$HOME` or absolute paths.
- Setting `status.showUntrackedFiles no` is essential to avoid seeing all Obsidian vault files in status.
- Some GUI Git tools and IDE integrations may not recognize this setup.
- Team collaboration requires everyone to understand and configure the same setup.

**Symlink considerations:**
- Always use relative paths for portability across machines.
- Git tracks the link, not the target content.
- Deleting the target doesn't affect the symlink in Git (creates a dangling reference).

**General limitation:**
- **No solution allows transparent, portable tracking of external files** except the bare repository approach, which requires explicit configuration.

### Recommendations

**Primary recommendation: Use the bare repository approach**

1. **Implementation:**
   ```bash
   # In your kh repository
   cd /home/user/Dev/kh/
   git init --bare .git-notes
   
   # Create alias (add to ~/.bashrc or ~/.zshrc)
   alias kh-notes='git --git-dir=/home/user/Dev/kh/.git-notes --work-tree=/home/user/Dev/Docs/.obs-vault/kh/notes'
   
   # Configure
   kh-notes config --local status.showUntrackedFiles no
   
   # Start tracking
   kh-notes add overview.md runbook.md locked.md
   kh-notes commit -m "Initial notes"
   ```

2. **Update your CLAUDE.md** to document this setup clearly.

3. **Create a helper script** (`bin/notes-git.sh`) to wrap common operations:
   ```bash
   #!/bin/bash
   git --git-dir=/home/user/Dev/kh/.git-notes \
       --work-tree=/home/user/Dev/Docs/.obs-vault/kh/notes \
       "$@"
   ```

4. **Consider integration with `/wrap` command** to automatically commit notes using the `kh-notes` alias.

**Alternative recommendation: Keep current symlink approach**

If the bare repository approach proves too complex for your workflow, the symlink approach is acceptable with these modifications:

1. **Reverse the symlink direction:**
   - Keep notes tracked in `kh/notes/`
   - Create symlink from vault pointing back: `/home/user/Dev/Docs/.obs-vault/kh/notes` → `/home/user/Dev/kh/notes`
   - Obsidian follows symlinks and will index the files

2. **This requires:**
   - Notes physically in `kh/notes/`
   - Obsidian configured to follow symlinks (most versions do by default)
   - Testing to ensure Obsidian plugins work correctly through symlinks

### Open Questions

- **How do Git hooks behave with the bare repository approach?** Your SessionEnd and SubagentStop hooks would need adjustment to use the `kh-notes` alias instead of standard `git` commands.

- **Performance implications:** Does Obsidian's indexing performance differ when files are symlinked vs. native? This may require empirical testing.

- **Team collaboration:** If others join the project, how complex is onboarding with the bare repository setup? Documentation burden may be significant.

- **Backup strategy:** Should the `.git-notes` bare repository be backed up separately or included in your main kh repository backup strategy?

### Sources

1. [Git Directory and Work-Tree Explained - jdhao's digital space](https://jdhao.github.io/2020/12/25/git_directory_work-tree_explained/) - Comprehensive explanation of `--git-dir` and `--work-tree`
2. [How to move/separate the .git folder out of your working tree - rakhesh.com](https://rakhesh.com/coding/how-to-move-separate-the-git-folder-out-of-your-working-tree/) - Practical guide to separating Git metadata from working tree
3. [How to Store Dotfiles - A Bare Git Repository - Atlassian](https://www.atlassian.com/git/tutorials/dotfiles) - Authoritative guide on bare repository approach for external file tracking
4. [Symbolic links in Git - mokacoding](https://mokacoding.com/blog/symliks-in-git/) - How Git tracks symlinks and relative vs. absolute path considerations
5. [Git Subtree vs. Git Submodule - GeeksforGeeks](https://www.geeksforgeeks.org/git/git-subtree-vs-git-submodule/) - Comparison of submodules and subtrees
6. [Git Worktree Documentation](https://git-scm.com/docs/git-worktree) - Official documentation on worktrees
7. [Using Git Worktrees for Multiple Working Directories - GeeksforGeeks](https://www.geeksforgeeks.org/git/using-git-worktrees-for-multiple-working-directories/) - Worktree practical usage
8. [Git Sparse-checkout Documentation](https://git-scm.com/docs/git-sparse-checkout) - Official documentation on sparse checkout
9. [Mount --bind - like symlinks only better!](https://edmondscommerce.github.io/linux/mount-bind-like-symlinks-only-better.html) - Bind mount vs symlink comparison
10. [The Bare Repo Approach to Storing Home Directory Config Files - DEV Community](https://dev.to/bowmanjd/store-home-directory-config-files-dotfiles-in-git-using-bash-zsh-or-powershell-the-bare-repo-approach-35l3) - Production usage of bare repositories

---

## Key Sources

*No high-relevance sources identified*

**Full sources:** [[research/outputs/OUTPUT-20260120-011140-ways-to-have-git-track-files-that/sources]]

---

## Outcome

**Decision:** *[To be determined]*

**Confidence:** Medium

**Rationale:** *[To be filled]*

**Next Steps:**
- Review findings
- *[Add next steps]*
