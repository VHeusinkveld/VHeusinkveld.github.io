# hveld.com

Vincent Heusinkveld's personal website. Built with Jekyll and hosted on GitHub Pages.

## Develop

With Ruby and Bundler installed:

```sh
bundle install
bundle exec jekyll serve
```

Open `http://localhost:4000`. The design uses local CSS and system fonts; navigation works without JavaScript.

## Content

- `aboutme.md`: biography, experience and education.
- `_posts/`: dated Markdown articles. Existing article permalinks are retained.
- `_layouts/home.html`: homepage introduction and writing archive.
- `assets/css/site.css`: responsive design, keyboard focus, reduced motion and print styles.
- `_config.yml`: site metadata and social profiles.
- `CNAME`: existing custom domain; keep `hveld.com`.

Post previews use the original `subtitle`, falling back to the article excerpt. Images use the existing `thumbnail-img` field. Add posts with the same front matter as the existing articles.

## Validate

```sh
JEKYLL_ENV=production bundle exec jekyll build
python3 tests/check_site.py _site
```

GitHub Actions builds and checks every push and pull request, and uploads the rendered site as the `website-preview` artifact. The checks cover the existing public routes, local links and anchors, semantic landmarks, image descriptions, titled embeds and removal of legacy runtime dependencies.

GitHub Pages and the existing domain remain the publishing path. The redesign does not require a hosting migration.

Originally based on [Beautiful Jekyll](https://beautifuljekyll.com) by Dean Attali; original license retained in `LICENSE`.
