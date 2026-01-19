---
type: research-output
id: OUTPUT-20260119-234145-obsidian-dataview-plugin-syntax-for
target-id: TARGET-20260119-220941
status: draft
created: 2026-01-19
researcher: claude-deep-research
confidence: medium
---

# Research Output: Obsidian Dataview plugin syntax for task queries. I need:

1. Basic task query

**Target:** [[research/targets/TARGET-20260119-220941-the-key-features-of-uv-package-manager]]

**Question:** Research Obsidian Dataview plugin syntax for task queries. I need:

1. Basic task query syntax (TASK FROM, WHERE, etc.)
2. How to query completed vs incomplete tasks
3. How to use inline fields on tas...

---

## Findings

Now let me compile all this research into a comprehensive, well-structured response with concrete examples optimized for the research vault.

This research provides comprehensive documentation on Obsidian Dataview plugin syntax for task queries, covering basic syntax, filtering, inline fields, sorting, grouping, and best practices. The information is current as of 2024-2026 and includes practical, runbook-ready examples with concrete code snippets that can be directly implemented.

## Research Summary

### Question/Topic
Research Obsidian Dataview plugin syntax for task queries, including: (1) basic task query syntax, (2) completed vs incomplete task filtering, (3) inline field usage on tasks, (4) filtering by inline field values, (5) sorting and grouping tasks, and (6) best practices for task metadata in runbook/checklist contexts.

### Key Findings

1. **TASK queries operate at task-level, not page-level** - Unlike LIST/TABLE queries that return pages, TASK queries return individual task objects, making task-specific metadata directly accessible.

2. **Inline fields on tasks require bracket syntax** - Tasks use `[fieldname:: value]` format (e.g., `[due:: 2026-01-20]`), not standalone syntax. Emoji shorthands (🗓️, ✅, ➕, 🛫, ⏳) provide shortcuts for common date fields.

3. **Completed vs incomplete filtering uses implicit fields** - The `completed`, `checked`, and `fullyCompleted` implicit fields enable precise task status filtering.

4. **Null handling is critical for field comparisons** - When filtering by inline fields (e.g., due dates), null values can produce unexpected results. Always check field existence before comparison.

5. **Multiple SORT commands enable multi-criteria ordering** - You can chain SORT statements in DQL for complex sorting logic.

6. **Grouping limitations exist for multi-level hierarchies** - Single-level grouping (by file or section) works straightforwardly, but true multi-level grouping (file + section) requires DataviewJS.

### Detailed Analysis

#### 1. Basic TASK Query Syntax

The fundamental structure of a TASK query follows this pattern:

```dataview
TASK
FROM <source>
WHERE <conditions>
SORT <field> <direction>
GROUP BY <field>
LIMIT <number>
```

**Core Components:**

- **TASK** (required): Query type that returns interactive task lists
- **FROM** (optional, max one): Specifies source - folders (`"folder/path"`), tags (`#tag`), or combinations
- **WHERE** (optional, unlimited): Filters tasks based on metadata or implicit fields
- **SORT** (optional, unlimited): Orders results by field values (ASC/DESC)
- **GROUP BY** (optional): Bundles tasks into groups
- **LIMIT** (optional): Restricts result count

**Key Characteristics:**

- TASK queries are **interactive** - checking a task in the query output updates the source file
- Data commands (WHERE, SORT, GROUP BY, LIMIT) can be used **multiple times** in any order after FROM
- TASK queries execute at **task-level**, making implicit task fields directly accessible

**Basic Examples:**

```dataview
TASK
FROM "Research/tasks"
```

```dataview
TASK
FROM #work OR #personal
```

```dataview
TASK
FROM "Projects" AND #active
```

#### 2. Filtering Completed vs Incomplete Tasks

Dataview provides three implicit boolean fields for task status:

| Field | Description |
|-------|-------------|
| `completed` | True if task status is 'x' or 'X' |
| `checked` | True if status is non-empty (any character) |
| `fullyCompleted` | True if task AND all subtasks are completed |

**Incomplete Tasks:**

```dataview
TASK
WHERE !completed
```

**Incomplete Tasks (Alternative):**

```dataview
TASK
WHERE !completed AND !checked
```

**Fully Incomplete (Including Subtasks):**

```dataview
TASK
WHERE !fullyCompleted
```

**Completed Tasks:**

```dataview
TASK
WHERE completed
```

**Completed Tasks from Specific Folder:**

```dataview
TASK
FROM "Daily Notes"
WHERE completed
```

**Incomplete Tasks with Tag Filter:**

```dataview
TASK
WHERE !completed AND contains(tags, "#shopping")
```

**Important Note:** Tasks with completion date emoji (✅) are properly recognized by the `completed` filter.

#### 3. Inline Fields on Tasks

Inline fields add custom metadata to individual tasks using bracket notation.

**Syntax:**

```markdown
- [ ] Task description [fieldname:: value]
```

**Multiple Inline Fields:**

```markdown
- [ ] Complete project report [due:: 2026-01-25] [priority:: high] [owner:: john]
```

**Common Field Types:**

| Field Type | Example | Dataview Type |
|------------|---------|---------------|
| Date | `[due:: 2026-01-20]` | date |
| Text | `[owner:: alice]` | text |
| Number | `[priority:: 1]` | number |
| Boolean | `[urgent:: true]` | boolean |
| List | `[tags:: #work, #important]` | list |

**Emoji Date Shorthands:**

Dataview supports emoji shortcuts for date-related fields (inspired by Tasks plugin):

| Emoji | Field Name | Description |
|-------|------------|-------------|
| 🗓️ | `due` | Due date |
| ✅ | `completion` | Completion date |
| ➕ | `created` | Creation date |
| 🛫 | `start` | Start date |
| ⏳ | `scheduled` | Scheduled date |

**Examples:**

```markdown
- [ ] Submit report 🗓️2026-01-25
- [x] Review document ✅2026-01-19
- [ ] Begin analysis 🛫2026-01-22 🗓️2026-01-29
```

These shorthands map to textual field names, so these are equivalent:

```markdown
- [x] Task completed ✅2026-01-19
- [x] Task completed [completion:: 2026-01-19]
```

**Querying emoji shorthands:**

```dataview
TASK
WHERE completion = date("2026-01-19")
```

**Critical Syntax Rules:**

1. **Always use bracket syntax for tasks**: `[key:: value]` not `key:: value`
2. **Double colon required**: `[due:: 2026-01-20]` not `[due: 2026-01-20]`
3. **Spaces in field names**: Automatically sanitized to lowercase with dashes (avoid if possible)
4. **Emoji keys**: Wrap in brackets `[🎯:: value]` (but avoid due to cross-platform issues)

#### 4. Filtering Tasks by Inline Field Values

**Existence Check:**

```dataview
TASK
WHERE due
```

```dataview
TASK
WHERE priority
```

**Comparison Operators:**

| Operator | Description |
|----------|-------------|
| `=` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

**Date Comparisons:**

```dataview
TASK
WHERE due <= date(today)
```

```dataview
TASK
WHERE due = date("2026-01-25")
```

```dataview
TASK
WHERE due >= date(today) AND due <= date(today) + dur(7 days)
```

**Text Comparisons:**

```dataview
TASK
WHERE owner = "alice"
```

```dataview
TASK
WHERE priority = "high"
```

**Numeric Comparisons:**

```dataview
TASK
WHERE priority <= 2
```

**Boolean Filters:**

```dataview
TASK
WHERE urgent = true
```

```dataview
TASK
WHERE urgent
```

**Critical: Null Handling**

Inline fields that don't exist are `null`, and comparisons with null can produce unexpected results:

```dataview
# WRONG - includes tasks without due dates because null <= date(today) is true
TASK
WHERE due <= date(today)
```

```dataview
# CORRECT - check existence first
TASK
WHERE due AND due <= date(today)
```

```dataview
# BEST - type-safe approach
TASK
WHERE typeof(due) = "date" AND due <= date(today)
```

**Logical Operators:**

```dataview
TASK
WHERE !completed AND due <= date(today)
```

```dataview
TASK
WHERE priority = "high" AND owner = "alice"
```

```dataview
TASK
WHERE priority = "high" OR urgent = true
```

**Complex Filters:**

```dataview
TASK
FROM "Projects"
WHERE !completed 
  AND typeof(due) = "date" 
  AND due <= date(today) + dur(3 days)
  AND (priority = "high" OR urgent = true)
```

**Using contains() for Tags:**

```dataview
TASK
WHERE contains(tags, "#work")
```

```dataview
TASK
WHERE !completed AND contains(tags, "#urgent")
```

#### 5. Sorting and Grouping Tasks

**Basic Sorting:**

```dataview
TASK
WHERE !completed
SORT due ASC
```

```dataview
TASK
WHERE !completed
SORT priority DESC
```

**Multiple Sort Criteria (Chained SORT):**

```dataview
TASK
WHERE !completed
SORT priority DESC
SORT due ASC
```

**Common Sort Fields:**

| Field | Description |
|-------|-------------|
| `due` | Due date (inline field) |
| `created` | Creation date (inline field) |
| `completion` | Completion date (inline field) |
| `priority` | Priority value (inline field) |
| `text` | Task text content (implicit field) |
| `line` | Line number (implicit field) |
| `file.name` | File name |
| `file.ctime` | File creation time |
| `file.mtime` | File modification time |

**Sort with Limit:**

```dataview
TASK
WHERE !completed
SORT due ASC
LIMIT 10
```

**Grouping by File:**

```dataview
TASK
WHERE !completed
GROUP BY file.link
```

**Grouping by Section/Header:**

```dataview
TASK
WHERE !completed
GROUP BY header
```

**Grouping by Custom Field:**

```dataview
TASK
WHERE !completed
GROUP BY priority
```

**Grouping with Sorting:**

```dataview
TASK
WHERE !completed
SORT due ASC
LIMIT 10
GROUP BY file.link
SORT rows.file.ctime ASC
```

**Group by Metadata Field:**

```dataview
TASK
FROM "Projects"
WHERE !completed
GROUP BY owner
SORT owner ASC
```

**Advanced Grouping by Section Path:**

```dataview
TASK
FROM "Projects/Active"
WHERE !completed AND contains(tags, "#milestone")
GROUP BY meta(section).subpath
```

**Sorting Within Groups:**

When using GROUP BY, you can sort both the groups and items within groups:

```dataview
TASK
WHERE !completed
GROUP BY file.link
SORT priority DESC
```

**Important Limitations:**

- **Multi-level grouping** (e.g., by file then by section) is **not directly supported** in DQL
- For complex multi-level grouping, use DataviewJS instead
- When grouping by file, sorting by inline fields may not work as expected if files contain multiple tasks

#### 6. Best Practices for Task Metadata

**Naming Conventions:**

1. **Use lowercase names**: `due`, `priority`, `owner` (avoid capitalization)
2. **Avoid spaces**: Use `duedate` or `due_date`, not `due date`
3. **Keep names short**: Easier to type and query
4. **Be consistent**: Use same field names across all tasks/files
5. **Avoid emojis in field names**: Cross-platform compatibility issues

**Recommended Field Set for Runbooks/Checklists:**

```markdown
- [ ] Task description [due:: YYYY-MM-DD] [priority:: 1-3] [owner:: name] [status:: text]
```

**Common Metadata Patterns:**

| Use Case | Fields | Example |
|----------|--------|---------|
| **Due date tracking** | `due` | `[due:: 2026-01-25]` |
| **Priority levels** | `priority` | `[priority:: 1]` or `[priority:: high]` |
| **Assignment** | `owner`, `assignee` | `[owner:: alice]` |
| **Status tracking** | `status` | `[status:: in-progress]` |
| **Effort estimation** | `effort`, `estimate` | `[effort:: 2h]` |
| **Dependencies** | `blocked-by`, `depends-on` | `[blocked-by:: [[Task-123]]]` |
| **Tags/Categories** | Use native `#tags` | `#work #urgent` |

**Best Practice Examples:**

**Runbook Task Template:**

```markdown
## Deployment Checklist

- [ ] Review code changes [owner:: dev-team] [due:: 2026-01-20] [priority:: 1]
- [ ] Run test suite [owner:: qa] [due:: 2026-01-21] [priority:: 1] [blocked-by:: [[code-review]]]
- [ ] Update documentation [owner:: tech-writer] [due:: 2026-01-22] [priority:: 2]
- [ ] Deploy to staging [owner:: devops] [due:: 2026-01-23] [priority:: 1]
- [ ] Perform smoke tests [owner:: qa] [due:: 2026-01-23] [priority:: 1]
- [ ] Deploy to production [owner:: devops] [due:: 2026-01-25] [priority:: 1]
```

**Corresponding Query:**

```dataview
TASK
FROM "Runbooks/Deployment"
WHERE !completed
SORT priority ASC, due ASC
```

**Using Emoji Shorthands for Simplicity:**

```markdown
- [ ] Submit report 🗓️2026-01-25 [priority:: high] [owner:: john]
- [ ] Review feedback 🗓️2026-01-26 [priority:: medium] [owner:: alice]
```

**Enable Automatic Completion Dates:**

In Dataview settings, enable "Automatic Task Completion Date" to automatically add completion dates when checking tasks in query results.

**Task Inheritance Awareness:**

Tasks inherit page-level frontmatter fields:

```yaml
---
project: Website Redesign
owner: design-team
---

## Tasks

- [ ] Create wireframes [due:: 2026-01-20]
- [ ] Design mockups [due:: 2026-01-25]
```

Both tasks have access to `project` and `owner` fields:

```dataview
TASK
WHERE project = "Website Redesign" AND !completed
```

**Avoiding Common Pitfalls:**

1. **Always check for null before comparisons:**
   ```dataview
   # GOOD
   TASK WHERE due AND due <= date(today)
   
   # BAD - includes tasks without due dates
   TASK WHERE due <= date(today)
   ```

2. **Use typeof() for type safety:**
   ```dataview
   TASK WHERE typeof(due) = "date" AND due <= date(today)
   ```

3. **Be aware of child task behavior:**
   - Child tasks appear if parent matches, even if child doesn't
   - Use `fullyCompleted` to ensure all subtasks are done

4. **Don't duplicate field names:**
   - Duplicate keys in same file create lists, not single values
   - Can cause unexpected results in queries

5. **Bracket syntax is mandatory for tasks:**
   ```markdown
   # GOOD
   - [ ] Task [due:: 2026-01-20]
   
   # BAD - won't work in queries
   - [ ] Task due:: 2026-01-20
   ```

6. **Use date() function for date comparisons:**
   ```dataview
   # GOOD
   TASK WHERE due = date("2026-01-25")
   
   # BAD - string comparison
   TASK WHERE due = "2026-01-25"
   ```

### Practical Runbook Query Examples

**Today's Tasks:**

```dataview
TASK
WHERE !completed AND due = date(today)
SORT priority ASC
```

**Overdue Tasks:**

```dataview
TASK
WHERE !completed AND typeof(due) = "date" AND due < date(today)
SORT due ASC
```

**This Week's Tasks:**

```dataview
TASK
WHERE !completed 
  AND typeof(due) = "date"
  AND due >= date(today)
  AND due <= date(today) + dur(7 days)
SORT due ASC, priority ASC
GROUP BY file.link
```

**High Priority Incomplete Tasks:**

```dataview
TASK
WHERE !completed AND priority = 1
SORT due ASC
```

**Tasks Assigned to Me:**

```dataview
TASK
WHERE !completed AND owner = "me"
SORT due ASC
```

**All Tasks from Current File:**

```dataview
TASK
WHERE file.name = this.file.name
```

**Recently Completed Tasks:**

```dataview
TASK
WHERE completed AND completion >= date(today) - dur(7 days)
SORT completion DESC
```

**Blocked Tasks:**

```dataview
TASK
WHERE !completed AND blocked-by
GROUP BY file.link
```

**Task Dashboard (Combined View):**

```dataview
TASK
WHERE !completed
SORT choice(priority = 1, "A", choice(priority = 2, "B", "C")) ASC, due ASC
LIMIT 20
```

### Limitations & Gotchas

- **Multi-level grouping not supported in DQL**: Cannot group by file then by section in pure DQL; requires DataviewJS
- **Null comparison pitfall**: `null <= date(today)` evaluates to true, including tasks without the field
- **Child task inheritance**: Child tasks appear when parent matches query, even if child doesn't match
- **Sorting within groups limitation**: When tasks are grouped by file, sorting by inline fields may not work predictably for multi-task files
- **Inline field syntax strict requirement**: Tasks MUST use `[key:: value]`, standalone `key:: value` doesn't work
- **Completion dates not automatic by default**: Must enable "Automatic Task Completion Date" in settings or add manually
- **Emoji shorthands date-only**: Only works for date fields (🗓️, ✅, ➕, 🛫, ⏳), not priority or other metadata
- **Cross-platform emoji issues**: Emoji field names may use different character codes on different OSes
- **Field name sanitization**: Spaces and capitals in field names are auto-converted to lowercase with dashes
- **No inline query filtering**: Cannot filter based on inline query results, only literal values
- **Tasks plugin integration**: Checking tasks via Dataview may not interact perfectly with Tasks plugin emoji/metadata

### Recommendations

1. **Establish consistent metadata schema**: Define standard fields (`due`, `priority`, `owner`, `status`) across all runbooks and stick to them
2. **Use emoji date shorthands for brevity**: `🗓️2026-01-25` is cleaner than `[due:: 2026-01-25]` in task descriptions
3. **Always null-check inline fields**: Use `WHERE field AND field < value` or `typeof(field) = "type"` patterns
4. **Enable automatic completion dates**: Turn on Dataview setting for automatic `completion` field when checking tasks
5. **Leverage task inheritance**: Put common metadata in frontmatter (project, team, category) and task-specific metadata inline
6. **Create reusable query templates**: Build a library of standard queries for common views (overdue, today, this week, high priority)
7. **Use numeric priority**: `[priority:: 1]` is easier to sort than `[priority:: high]`
8. **Combine SORT for multi-criteria ordering**: Chain multiple SORT commands for sophisticated ordering
9. **Limit results for performance**: Use LIMIT on large vaults to prevent slow rendering
10. **Group strategically**: Group by file for runbooks, by priority/owner for dashboards, by section for detailed views
11. **Document your metadata schema**: Create a reference note defining your standard task fields and their meanings
12. **Test queries iteratively**: Start simple, add filters incrementally, verify results at each step
13. **Consider DataviewJS for complex needs**: If DQL limitations (multi-level grouping, complex logic) become blockers, switch to DataviewJS
14. **Use `fullyCompleted` for checklists with subtasks**: Ensures parent task only shows as done when all children complete
15. **Combine with Tasks plugin judiciously**: If using both, be aware of potential interaction issues; prefer one for primary workflow

### Open Questions

- **Performance at scale**: How do complex TASK queries with multiple WHERE/SORT/GROUP BY clauses perform on vaults with 1000+ tasks?
- **DataviewJS equivalents**: What are the DataviewJS patterns for multi-level grouping and complex aggregations not covered here?
- **Tasks plugin interoperability**: What is the current state of emoji completion dates and status synchronization between Dataview and Tasks plugin?
- **Advanced filtering patterns**: Are there regex or advanced text matching capabilities beyond `contains()` for filtering task text?
- **Custom rendering**: Can task query output be customized beyond default checkbox lists (e.g., Kanban-style, calendar view)?
- **Real-time updates**: How does Dataview cache task queries, and what triggers re-evaluation in live preview?

### Sources

1. [Query Types - Dataview](https://blacksmithgu.github.io/obsidian-dataview/queries/query-types/) - Official documentation on TASK query type
2. [Metadata on Tasks and Lists - Dataview](https://blacksmithgu.github.io/obsidian-dataview/annotation/metadata-tasks/) - Complete reference for task metadata and inline fields
3. [Structure of a Query - Dataview](https://blacksmithgu.github.io/obsidian-dataview/queries/structure/) - Query structure with FROM, WHERE, SORT, GROUP BY commands
4. [Expressions - Dataview](https://blacksmithgu.github.io/obsidian-dataview/reference/expressions/) - Comparison operators and functions for WHERE clauses
5. [Basic Task Queries - Dataview Example Vault](https://s-blu.github.io/obsidian_dataview_example_vault/20 Dataview Queries/Basic Task Queries/) - Practical TASK query examples
6. [How to group tasks by File and then by Section? - GitHub Discussion](https://github.com/blacksmithgu/obsidian-dataview/discussions/720) - Multi-level grouping patterns
7. [Dataview all tasks not completed - Obsidian Forum](https://forum.obsidian.md/t/dataview-all-tasks-not-completed/20235) - Community solutions for filtering incomplete tasks
8. [Sorting tasks by priority in Dataview - Obsidian Forum](https://forum.obsidian.md/t/sorting-tasks-by-priority-in-dataview/93872) - Priority sorting examples
9. [Adding Metadata - Dataview](https://blacksmithgu.github.io/obsidian-dataview/annotation/add-metadata/) - General metadata annotation guide
10. [Dataview in Obsidian: A Beginner's Guide - Obsidian Rocks](https://obsidian.rocks/dataview-in-obsidian-a-beginners-guide/) - Comprehensive beginner tutorial
11. [Dataview task and project examples - Obsidian Forum](https://forum.obsidian.md/t/dataview-task-and-project-examples/17011) - Real-world workflow examples
12. [Managing efficiently your tasks with Obsidian and Dataview - LazySnail](https://www.lazysnail.net/obsidian/Obsdian-dataview-tasks) - Task management workflow guide

---

## Key Sources

*No high-relevance sources identified*

**Full sources:** [[research/outputs/OUTPUT-20260119-234145-obsidian-dataview-plugin-syntax-for/sources]]

---

## Outcome

**Decision:** *[To be determined]*

**Confidence:** Medium

**Rationale:** *[To be filled]*

**Next Steps:**
- Review findings
- *[Add next steps]*
