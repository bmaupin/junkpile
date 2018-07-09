import fs from 'fs';
import GoogleSitesConverter from '../GoogleSitesConverter';

test('Convert page with code', async () => {
  let markdown = fs.readFileSync('./__tests__/resources/clamav.md').toString('utf8');
  let converted = await GoogleSitesConverter.convertFromFile('./__tests__/resources/clamav.html');
  expect(converted).toBe(markdown);
});
