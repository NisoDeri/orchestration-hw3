from chromatic_crew.orchestration import briefs
from chromatic_crew.orchestration.outline import SectionSpec, Slot


def _section(**kw):
    base = {
        "id": "s",
        "title_en": "Title",
        "title_he": "כותרת",
        "language": "en",
        "target_words": 100,
        "purpose": "p",
        "key_points": ["k1"],
        "slots": [],
    }
    base.update(kw)
    return SectionSpec(**base)


def test_writer_brief_english():
    brief = briefs.writer_brief(_section())
    assert "DEADPAN" in brief
    assert "## Title" in brief
    assert "Write in English." in brief


def test_writer_brief_hebrew_drafts_english_first():
    brief = briefs.writer_brief(_section(language="he"))
    assert "translated to Hebrew" in brief


def test_writer_brief_includes_formula_slot():
    brief = briefs.writer_brief(_section(slots=[Slot("formula", "PK", "C(t) closed form")]))
    assert "[PK]" in brief


def test_translator_brief():
    assert "ACADEMIC HEBREW" in briefs.translator_brief("some english")


def test_figure_and_tikz_briefs():
    assert "matplotlib" in briefs.figure_brief("F1", "a curve")
    assert "tikzpicture" in briefs.tikz_brief("D1", "a pipeline")
