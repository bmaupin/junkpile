import fs from 'fs';
import GoogleSitesConverter from '../GoogleSitesConverter';

test('Convert page with code', async () => {
  let markdownFromFile = fs.readFileSync('./__tests__/resources/clamav.md').toString('utf8');
  let convertedMarkdown = await GoogleSitesConverter.convertFromFile('./__tests__/resources/clamav.html');
  expect(convertedMarkdown).toBe(markdownFromFile);
});

test('Convert page with code in a list', async () => {
  let markdownFromFile = fs.readFileSync('./__tests__/resources/cups.md').toString('utf8');
  let convertedMarkdown = await GoogleSitesConverter.convertFromFile('./__tests__/resources/cups.html');
  expect(convertedMarkdown).toBe(markdownFromFile);
});
