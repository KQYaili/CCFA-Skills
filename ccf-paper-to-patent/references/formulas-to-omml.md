# Formulas to OMML: Handling Note

> Reference note for ccf-paper-to-patent. The upstream conversion
> script (Yuan1z0825/nature-skills, `math_to_omml.py`, Apache
> License 2.0) is **not imported**: it depends on the external
> `python-docx` package (`docx.oxml`), which this repository does not
> vendor, so the conversion is described here as a protocol step
> instead of shipped code.

## Why OMML

CNIPA-facing DOCX drafts need equations as native Office Math Markup
Language (OMML) objects, not images and not raw LaTeX text, so that
examiners and agents can edit them. The structured draft therefore
stores every equation's LaTeX source (required by
[draft-schema.md](draft-schema.md)); conversion happens at document
render time.

## Conversion protocol

1. Keep the LaTeX source, symbol definitions, and technical role in
   the draft JSON; never store only a rendered form.
2. At DOCX rendering, convert each equation's LaTeX to OMML with a
   converter available in the host environment (the upstream approach
   builds the OMML tree via `python-docx`'s XML layer). If no
   converter is available, deliver the draft with equations as LaTeX
   and label the package incomplete for filing purposes.
3. After conversion, visually verify each equation in the rendered
   document against the source formula: subscripts, fraction scope,
   and symbol identity are the usual corruption points, and no
   automated check in this repository covers them.
4. Never silently simplify a formula during conversion; a
   simplification is a `formula_inventory` disposition decision made
   at Stage 2, recorded with its reason.
