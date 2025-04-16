/*
 * Fetch pre-Civ 7 Polycast and Modcast feeds, merge them into one XML file
 *
 * To run:
 *
 * node --experimental-strip-types get-polycast-feed.ts
 *
 */

import fs from 'node:fs/promises';

import jsdom from 'jsdom';
const { JSDOM } = jsdom;
const dom = new JSDOM('');
const DOMParser = dom.window.DOMParser;

const feedUrls = [
  // This URL is first as it serves as the base for the merged feed
  'https://polycast.civfanatics.com/PolyCastOnly.xml',
  'https://polycast.civfanatics.com/polycast/season1.xml',
  'https://polycast.civfanatics.com/polycast/season2.xml',
  'https://polycast.civfanatics.com/polycast/season3.xml',
  'https://polycast.civfanatics.com/polycast/season4.xml',
  'https://polycast.civfanatics.com/polycast/season5.xml',
  'https://polycast.civfanatics.com/polycast/season6.xml',
  'https://polycast.civfanatics.com/polycast/season7.xml',
  'https://polycast.civfanatics.com/polycast/season8.xml',
  'https://polycast.civfanatics.com/polycast/season9.xml',
  'https://polycast.civfanatics.com/polycast/season10.xml',
  'https://polycast.civfanatics.com/polycast/season11.xml',
  'https://polycast.civfanatics.com/modcast/season1.xml',
  'https://polycast.civfanatics.com/modcast/season2.xml',
  'https://polycast.civfanatics.com/modcast/season3.xml',
  'https://polycast.civfanatics.com/modcast/season4.xml',
  'https://polycast.civfanatics.com/modcast/season5.xml',
  'https://polycast.civfanatics.com/modcast/season6.xml',
  'https://polycast.civfanatics.com/modcast/season7.xml',
  'https://polycast.civfanatics.com/modcast/season8.xml',
  'https://polycast.civfanatics.com/modcast/season9.xml',
  'https://polycast.civfanatics.com/modcast/season10.xml',
  'https://polycast.civfanatics.com/modcast/season11.xml',
];

const episodeSubstringsToFilterOut: string[] = [
  'Evergreen',
  'PolyCast Bloopers',
  'PolyCast Cut!',
  'PolyCast Promo',
  'TurnCast',
];

const episodesToFilterOut: string[] = [
  'PolyCast 433: Fringe Theories',
  'PolyCast 434: Zip! Give It To Me!',
  'PolyCast 435: So It Shall Be',
  'PolyCast 436: They Say Strategy is Dying',
  'PolyCast 437: Starting to Get Rolling',
  'PolyCast 438: Something to Believe In - Part 1',
  'PolyCast 439: Something to Believe In - Part 2',
  'PolyCast 440: PAX and Direct',
  'PolyCast Play-by-Play #01: Unification',
  'Support the PolyCast Patreon Campaign',
];

const EXTRA_PHP_TAGS = '";\n?>';

const main = async () => {
  const parsedFeeds = await Promise.all(feedUrls.map(fetchAndParseFeed));
  const mergedFeed = await mergeFeeds(parsedFeeds);
  await writeFile(mergedFeed);
};

const fetchAndParseFeed = async (url: string): Promise<Document> => {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Response status: ${response.status} fetching URL ${url}`);
  }

  let feedData = await response.text();
  feedData = removeExtraPhpTags(feedData);

  return new DOMParser().parseFromString(feedData, 'text/xml');
};

const removeExtraPhpTags = (data: string): string => {
  if (data.endsWith(EXTRA_PHP_TAGS)) {
    return data.slice(0, -EXTRA_PHP_TAGS.length);
  }
  return data;
};

// NOTE: This function is almost entirely from ChatGPT
async function mergeFeeds(parsedFeeds: Document[]): Promise<Document> {
  // Use the first valid feed as the base
  const baseFeed = parsedFeeds.find((feed) => feed !== null);
  if (!baseFeed) {
    throw new Error('No valid feeds were fetched.');
  }

  // Get the <channel> element of the base feed
  const baseChannel = baseFeed.querySelector('channel');
  if (!baseChannel) {
    throw new Error('Base feed is missing a <channel> element.');
  }

  baseChannel.querySelector('pubDate')!.textContent = new Date().toUTCString();

  baseChannel.querySelector('title')!.textContent = 'PolyCast and ModCast';
  baseChannel.querySelector('description')!.textContent =
    'PolyCast and ModCast up to but not including Civ 7';

  // Track existing GUIDs to prevent duplicates
  const seenGuids = new Set<string>();
  const allItems: Element[] = [];

  // Collect items from all feeds and ensure no duplicate GUIDs
  for (const feed of parsedFeeds) {
    if (!feed) continue;

    const items = feed.querySelectorAll('item');
    for (const item of items) {
      const title = item.querySelector('title')?.textContent;
      if (title && episodesToFilterOut.includes(title)) {
        console.log(`Filtered out episode: ${title}`);
        continue;
      }

      if (
        title &&
        episodeSubstringsToFilterOut.some((substring) => title.includes(substring))
      ) {
        console.log(`Filtered out episode: ${title}`);
        continue;
      }

      const guid = item.querySelector('guid')?.textContent;
      if (guid && seenGuids.has(guid)) {
        continue;
      }
      if (guid) {
        seenGuids.add(guid);
      }
      allItems.push(item);
    }
  }

  // Sort items by <pubDate> in descending order (most recent first)
  allItems.sort((a, b) => {
    const dateA = new Date(a.querySelector('pubDate')?.textContent || 0);
    const dateB = new Date(b.querySelector('pubDate')?.textContent || 0);
    return dateB.getTime() - dateA.getTime();
  });

  // Remove existing <item> elements in the base feed
  const baseItems = baseChannel.querySelectorAll('item');
  baseItems.forEach((item) => item.remove());

  // Append the sorted items to the base feed's <channel>
  for (const item of allItems) {
    const importedItem = baseFeed.importNode(item, true);
    baseChannel.appendChild(importedItem);
  }

  return baseFeed;
}

const writeFile = async (doc: Document): Promise<void> => {
  await fs.writeFile(
    'polycast-modcast.xml',
    doc.documentElement.outerHTML.replaceAll('\n', '\r\n')
  );
};

main();
