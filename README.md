# Serai Studio · client sites

One JSON file per client in `clients/`. Push to `main` and GitHub Actions builds every site and publishes it to GitHub Pages:

    https://preparedmale.github.io/client-sites/<slug>/        (first language)
    https://preparedmale.github.io/client-sites/<slug>/ru/     (other languages)

Add a client: copy a file in `clients/`, change `slug` and the content, put photos in `clients/<slug>/`, push.
Build locally: `python3 build.py` (output in `site/`).

Samples marked `"sample": true` are fictional businesses and carry a notice and `noindex`.
