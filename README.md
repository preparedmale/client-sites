# Serai Studio · client sites

One JSON file per client in `clients/`. Push to `main` and Cloudflare Pages builds every site and publishes it:

    https://serai-studio.pages.dev/<slug>/        (first language)
    https://serai-studio.pages.dev/<slug>/ru/     (other languages)

Cloudflare Pages project settings: production branch `main`, framework preset `None`,
build command `python3 build.py`, build output directory `site`.
If the public address changes (other pages.dev name or own domain), set the
environment variable `SITE_BASE` in the Pages project, e.g. `https://seraistudio.com`.

Add a client: copy a file in `clients/`, change `slug` and the content, put photos in `clients/<slug>/`, push.
Build locally: `python3 build.py` (output in `site/`).

Samples marked `"sample": true` are fictional businesses and carry a notice and `noindex`.
