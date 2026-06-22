# Module 3 · Structured Output

Free-form text is hard to use in code. **Structured output** forces the model to
return data in a shape you define — a typed object or a dict — so you can use it
directly: store it, branch on it, pass it to another function. This is the single
biggest reliability upgrade for any LLM app.

> Local models follow formatting instructions less reliably than frontier models,
> so this module also covers validation and automatic repair — read to the end.

## The two approaches

1. **`with_structured_output(Model)`** — easiest. You give a Pydantic class; LangChain
   handles the rest and hands back a typed object. **Start here.**
2. **Output parsers** (`JsonOutputParser`, `PydanticOutputParser`) — more control. You
   inject `format_instructions` into your prompt and parse the result yourself. Use
   when you need to see/tune the instructions or want a plain dict.

## The examples

### `01_with_structured_output.py` — the easy path
Define `TechSummary` with three fields, call `llm.with_structured_output(TechSummary)`,
get back a real object with `.technology`, `.one_liner`, `.difficulty`. Note how
`Field(description=...)` guides the model on what each field means.

### `02_nested_and_lists.py` — complex shapes
Schemas can nest. A `Recipe` contains a list of `Ingredient` objects and a list of
step strings, and the model fills the whole tree. This is how you model real data.

### `03_json_output_parser.py` — explicit control, plain dict
`JsonOutputParser(pydantic_object=Movie)` generates format instructions you insert into
the prompt with `.partial(...)`, then parses the model's JSON (fences and all) into a
dict. Use when you want to control the prompt wording.

### `04_retry_validation.py` — making it reliable ⭐
The important one for local models. Pydantic `@field_validator`s enforce real rules
(rating 1–5, sentiment in a fixed set). `OutputFixingParser` catches malformed output
and sends it *back to the model with the error* to be repaired automatically. This
combination turns a flaky small model into a dependable extractor.

### `05_extraction.py` — a real use case
Pull a list of people, roles, and organizations out of a paragraph into typed objects.
`Optional[str]` fields with defaults handle "not mentioned" gracefully. This pattern
(extraction into a list-of-models) is one of the most useful in practice.

## Choosing an approach (quick guide)

| You want… | Use |
|-----------|-----|
| Typed object, least code | `with_structured_output(Model)` |
| A plain dict | `JsonOutputParser` |
| Custom prompt wording | `JsonOutputParser` / `PydanticOutputParser` |
| Enforced constraints | Pydantic `@field_validator` |
| Auto-repair of bad output | `OutputFixingParser` |

## Tips for reliable structured output on local models

- Set `temperature=0` — randomness hurts formatting.
- Keep schemas flat and field names obvious; add a `description` to every field.
- Prefer enums-as-strings with a validator over free text for categorical fields.
- Wrap with `OutputFixingParser` for anything user-facing.

## Try this

1. Add a `confidence: float` field (0–1) to `01` with a validator that clamps it.
2. Change `05` to also extract any dates mentioned, as a list of strings.
3. Break `04` on purpose (ask for a rating of 11) and watch the fixing parser correct it.

## Next

Module 4 adds a **retrieval** step before the prompt so the model can answer from your
own documents (RAG).
