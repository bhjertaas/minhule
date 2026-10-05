# minhule.eu

The landing page for [minhule.eu](https://minhule.eu): a little cave of apps. Plain HTML and CSS, published with GitHub Pages.

- `index.html`, `style.css`: the page (light and dark colours via `prefers-color-scheme`).
- `lango/`: `minhule.eu/lango` redirects to [lango.minhule.eu](https://lango.minhule.eu).
- `404.html`: "Lost at sea".
- `images/`: illustrations made with an image model (gpt-image-2); the lanGo portraits (Lucía, and Alain in the corner) come from the lanGo repository. `scripts/make-image.py <name>` regenerates `images/<name>.webp` from `scripts/prompts/<name>.txt`, using `OPENAI_API_KEY` from `.env` (git-ignored).
- Visitor counts: [GoatCounter](https://minhule.goatcounter.com), cookieless. Button clicks are counted via `data-goatcounter-click`, and opened tech notes via `data-count` on the `<details>`.
- `CNAME`: the custom domain for GitHub Pages.

To add an app, add a card to the `.apps` list in `index.html` (and optionally a short-link folder like `lango/`).
