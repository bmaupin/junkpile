'use strict';

import GoogleSitesConverter from './GoogleSitesConverter';

async function main(): Promise<void> {
  if (process.argv.length < 3) {
    console.log('Usage: npm start URL');
    process.exit();
  }

  let url = process.argv[2];
  let markdown = await GoogleSitesConverter.convertPageFromUrl(url);
  // let markdown = await GoogleSitesConverter.convertPageFromFile('./__tests__/resources/clamav.html');
  console.log(markdown);
}

// https://stackoverflow.com/a/43994999/399105
process.on('unhandledRejection', (reason, p) => {
  console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
});

main();
