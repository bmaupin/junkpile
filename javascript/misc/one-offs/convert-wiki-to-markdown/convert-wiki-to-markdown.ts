'use strict';

import GoogleSitesConverter from './GoogleSitesConverter';

// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/clamav';
const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/cups';
// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/firefox';

async function main() {
  let markdown = await GoogleSitesConverter.convertSite(WIKI_URL);
  console.log(markdown);
}

// https://stackoverflow.com/a/43994999/399105
process.on('unhandledRejection', (reason, p) => {
  console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
});

main();
