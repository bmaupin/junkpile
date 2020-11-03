Small script to convert my old wiki at https://sites.google.com/site/bmaupinwiki/ to markdown for importing into my new wiki at https://bmaupin.github.io/wiki/

Usage:

1. Edit convert-wiki-to-markdown.ts
    1. Change `WIKI_URL` to the URL to convert
1. Run this script

    ```
    npm start --silent > /path/to/wiki/applications/misc/libreoffice.md
    ```

    Note: `--silent` is used to suppress superfluous output from being added to the output file
