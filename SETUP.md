# Nattt — Animated ASCII GitHub README

Compact, animated, self-contained SVG README inspired by the technique from https://www.avivashishta.com/blog/build-animated-github-profile-readme. Not a copy of the referenced profile’s artwork.

## Contents

- `assets/contributions.svg` — animated contribution graph (ships with a clearly marked preview; real data after workflow success)
- `assets/portrait.svg` — ASCII portrait converted from the avatar image you provided
- `assets/info.svg` — animated profile information
- `assets/stack.svg` — animated, typography-led tech stack; four groups
- `assets/footer.svg` — animated signature footer
- `assets/source-photo.png` — the uploaded avatar used to generate the ASCII portrait
- `scripts/*.py` — source generators (so SVGs can be regenerated)
- `.github/workflows/refresh-art.yml` — daily refresh of portrait and contributions

## Install

1. Extract ZIP and upload its contents to the root of your **`RahmatHadinata23758051/RahmatHadinata23758051`** profile repository, preserving folders. You don't need to upload preview PNGs or HTML.
2. Commit the files to `main`.
3. Open **Actions → Refresh profile artwork → Run workflow** once to attempt to replace the preview contribution chart with actual GitHub history. Check that GitHub Actions has write access if auto-commits fail.
4. To change the ASCII portrait, replace `assets/source-photo.png` with a different image and rerun the workflow; the generator prefers that file. The `--cutout` option was tailored for the bundled illustrated avatar. Remove the option from the workflow if a different portrait gets clipped.

**Note:** The initial contribution graphic is labeled as PREVIEW because it is not your real graph. The daily workflow attempts to fetch your public GitHub contributions, and does not overwrite the image if retrieval fails. The ASCII portrait, however, **already uses the image you supplied**.

## Local regenerate

```bash
python -m pip install -r scripts/requirements.txt
python scripts/make_ascii_svg.py --image assets/source-photo.png --cutout
python scripts/make_info_svg.py
python scripts/make_stack_svg.py
python scripts/make_footer_svg.py
python scripts/fetch_contributions.py && python scripts/make_heatmap_svg.py
```

Open `preview.html` locally to preview the animation in your browser.

## Compatibility

README itself contains only GitHub-compatible Markdown/HTML and image tags. Animations are self-contained SVG CSS/SMIL; different GitHub surfaces, browser settings and reduced-motion preferences can change how motion appears. In supported environments, no README JavaScript is required. SVG files are vector-sharp. Everything in the final display lives in your profile repository.
