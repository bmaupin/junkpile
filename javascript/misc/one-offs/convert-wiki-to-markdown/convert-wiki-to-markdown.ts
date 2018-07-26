'use strict';

import GoogleSitesConverter from './GoogleSitesConverter';

// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/clamav';
// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/cups';
// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/firefox';
const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/programming/tools/meld';

async function main(): Promise<void> {
  let markdown = await GoogleSitesConverter.convertFromUrl(WIKI_URL);
  // let markdown = await GoogleSitesConverter.convertFromFile('./__tests__/resources/clamav.html');
  console.log(markdown);
}

// https://stackoverflow.com/a/43994999/399105
process.on('unhandledRejection', (reason, p) => {
  console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
});

main();
