# Proposed Changes - Semantic Distillation Pipeline

## Open Question: Output Format

### Research Paper Proposal
```
# MANIFEST
# UNIFIED TYPES (TypeScript-like)
# MODULES (signatures grouped by domain)
# PATTERNS (3-5 examples)
```

### Concerns
- This format is theoretical, not battle-tested
- Existing successful LLM documentation uses simpler formats
- Token-efficient code examples + short explanations is "proven"
- May be over-engineered for the use case

### Alternative: Proven Format
```
## Concept Name
One-line explanation.

\`\`\`jac
minimal_working_example();
\`\`\`
```

### TODO: Evaluate Formats
- [ ] Survey existing LLM-optimized docs (llms.txt, cursor rules, etc.)
- [ ] Compare token efficiency of different formats
- [ ] Test LLM performance with different output structures
- [ ] Decide on format based on empirical results, not theory

---

## Pending Changes

### Module Resolution Map
Add import path mapping so LLM generates correct imports:
```
@map: Walker -> /jac/core/walker.jac
```

### EBNF Grammar Injection
Include minimal grammar rules for Jac syntax:
```ebnf
edge_op ::= "++" ">" | "--" ">"
```

### Style Manifesto
Explicit coding conventions embedded in output.

### Few-Shot Example Selection
"Rule of Three": basic usage, edge case, integration example.

---

## Target

Output size: 116KB -> 10-20KB (need 5-10x more compression)

Format decision should be data-driven, not theory-driven.
