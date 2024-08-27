#!/usr/bin/env python


import sys
from datetime import date
from pathlib import Path
from typing import Any

import fontforge
import psMat
from math import radians

from mmtool import font_action
from mmtool.data import Style, Target, REPO_DIST
from mmtool.unicode import block_width_of, unicode_block_of, target_width_of

GENEI_TRANSFORMS: dict[tuple[str, bool], Any] = {
    ("uniform", False): font_action.compose_transforms([
        psMat.scale(1.1, 1.1),
        psMat.translate(102, 0)
    ]),
    ("full2half", False): font_action.compose_transforms([
        psMat.scale(0.8, 0.8),
        psMat.translate(-205, 0)
    ]),
    ("half2full", False): font_action.compose_transforms([
        psMat.scale(1.25, 1.25),
        psMat.translate(589, 0)
    ]),
    ("uniform", True): font_action.compose_transforms([
        psMat.scale(1.1, 1.1),
        psMat.skew(radians(9)),
        psMat.translate(102, 0)
    ]),
    ("full2half", True): font_action.compose_transforms([
        psMat.scale(0.8, 0.8),
        psMat.skew(radians(9)),
        psMat.translate(-205, 0)
    ]),
    ("half2full", True): font_action.compose_transforms([
        psMat.scale(1.25, 1.25),
        psMat.skew(radians(9)),
        psMat.translate(589, 0)
    ]),
}

VERSION = f"1.1-{date.today()}"
TARGETS = {
    "MomiageMono-Regular.ttf": Target(
        VERSION,
        Style(None, False),
        "GenEiMonoGothic-Regular.ttf",
        "JetBrainsMono-Regular.ttf"
    ),
    "MomiageMono-Italic.ttf": Target(
        VERSION,
        Style(None, True),
        "GenEiMonoGothic-Regular.ttf",
        "JetBrainsMono-Italic.ttf"
    ),
    "MomiageMono-Bold.ttf": Target(
        VERSION,
        Style("Bold", False),
        "GenEiMonoGothic-Bold.ttf",
        "JetBrainsMono-Bold.ttf"
    ),
    "MomiageMono-BoldItalic.ttf": Target(
        VERSION,
        Style("Bold", True),
        "GenEiMonoGothic-Bold.ttf",
        "JetBrainsMono-BoldItalic.ttf"
    ),
}


def _copy_genei_mono_gothic(font: fontforge.font, target: Target):
    make_oblique = target.style().is_italic()

    gemg_font = fontforge.open(target.gemg_path())
    gemg_font.em = 2048

    gemg_font.selection.all()
    gemg_glyph_names = []
    for glyph in gemg_font.selection.byGlyphs:
        if glyph.unicode == -1:
            continue

        block = unicode_block_of(glyph.unicode)
        block_info = block_width_of(block[2])
        if block_info is None:
            continue

        block_font_tag = block_info[1]
        if block_font_tag is not None and block_font_tag != "gemg":
            continue

        # TODO: deal with zero-width glyph
        glyph_width = "full" if glyph.width / 2048 > 0.95 else "half"
        target_width = target_width_of(glyph.unicode)

        if glyph_width == target_width:
            glyph.transform(GENEI_TRANSFORMS[("uniform", make_oblique)])
        elif glyph_width == "full":
            glyph.transform(GENEI_TRANSFORMS[("full2half", make_oblique)])
        elif glyph_width == "half":
            glyph.transform(GENEI_TRANSFORMS[("half2full", make_oblique)])
        glyph.width = 2456 if target_width == "full" else 1228

        gemg_glyph_names.append(glyph.glyphname)

    font_action.create_insufficient_slots(font, gemg_glyph_names)
    font_action.copy_glyphs(font, gemg_font, gemg_glyph_names)

    gemg_font.close()


def _copy_jetbrains_mono(font: fontforge.font, target: Target):
    jbm_font = fontforge.open(target.jbm_path())
    jbm_font.em = 2048

    font.importLookups(jbm_font, jbm_font.gsub_lookups)
    font.importLookups(jbm_font, jbm_font.gpos_lookups)

    jbm_glyph_names = font_action.fetch_glyph_names(jbm_font, None)
    font_action.create_insufficient_slots(font, jbm_glyph_names)
    font_action.copy_glyphs(font, jbm_font, jbm_glyph_names)

    jbm_font.close()


def generate_momiage_mono(target: Target, filename: Path):
    # Momiage Mono
    font = fontforge.font()
    font.encoding = "UnicodeFull"
    font_action.set_metrics(font)

    # GenEi Mono Gothic
    print("=> Copying glyphs from GenEi Mono Gothic")
    _copy_genei_mono_gothic(font, target)

    # JetBrains Mono
    print("=> Copying glyphs from JetBrains Mono")
    _copy_jetbrains_mono(font, target)

    # Finalize
    font_action.set_info(font, target)
    font.generate(
        str(filename),
        "",
        ("short-post", "PfEd-lookups", "opentype")
    )


def main():
    filename = sys.argv[1]
    generate_momiage_mono(TARGETS[filename], REPO_DIST / filename)


if __name__ == "__main__":
    main()
