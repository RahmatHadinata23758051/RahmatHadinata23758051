# Nattt · Animated ASCII GitHub Profile

Inspired by the *technique* from Avi Vashishta's article: https://www.avivashishta.com/blog/build-animated-github-profile-readme

No reference SVG or portrait has been copied. The Python scripts create self-contained SVG artwork.

## How to install

1. Extract this ZIP to the root of `RahmatHadinata23758051/RahmatHadinata23758051` (preserve `scripts/`, `assets/`, and `.github/workflows/`).
2. (Recommended) Put a clear headshot at `assets/source-photo.jpg` or `assets/source-photo.png`. Use a simple/light background, head and shoulders visible, preferably a portrait rather than a cropped circular icon.
3. Push the files to `main`.
4. Go to GitHub **Actions** → **Refresh profile artwork** → **Run workflow**.
5. The workflow generates a personal ASCII portrait (your local image takes priority; otherwise it fetches your GitHub avatar), creates the animated information card, and attempts to fetch genuine public GitHub contributions.

**Important:** the ZIP includes an initial placeholder ASCII wordmark, not your actual facial portrait. It is labeled `PREVIEW ONLY`. The generated portrait can only genuinely resemble you once a real source photo is available. The initial contributions calendar is also labeled PREVIEW; it is not fabricated data. GitHub Actions replaces it with real data on successful retrieval.

## Local use

```bash
python -m pip install -r scripts/requirements.txt
python scripts/make_ascii_svg.py --image /path/to/photo.jpg
python scripts/make_info_svg.py
python scripts/fetch_contributions.py
python scripts/make_heatmap_svg.py
```

Or use the GitHub avatar without uploading a new photo:

```bash
python scripts/make_ascii_svg.py --fetch-avatar
```

Open `preview.html` in a browser to see the animation with the current SVG assets.

## GitHub compatibility

The README itself only uses HTML and references SVGs with `<img>`. Motion uses SMIL and CSS inside each separate SVG file. GitHub's image sanitization and browser preferences may vary; if your browser disables animation or reduced-motion settings are active, motion can be suppressed.

The scheduled workflow runs once a day. GitHub contribution markup is not a stable documented API; the fetcher refuses to invent values or overwrite the existing graph if it cannot parse enough entries.
