/*
 * Fetch all old Polycast and Modcast feeds, merge them into one XML file
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
  'https://polycast.civfanatics.com/modcast/season1.xml',
  'https://polycast.civfanatics.com/modcast/season2.xml',
  'https://polycast.civfanatics.com/modcast/season3.xml',
  'https://polycast.civfanatics.com/modcast/season4.xml',
  'https://polycast.civfanatics.com/modcast/season5.xml',
  'https://polycast.civfanatics.com/modcast/season6.xml',
  'https://polycast.civfanatics.com/modcast/season7.xml',
  'https://polycast.civfanatics.com/modcast/season8.xml',
  'https://polycast.civfanatics.com/modcast/season9.xml',
];

const episodeSubstringsToFilterOut = [
  'PolyCast Bloopers',
  'PolyCast Cut!',
  'PolyCast Promo',
  'TurnCast',
];

const episodesToFilterOut = [
  'ModCast #67: Newborn Smell',
  'ModCast #69: Laying Foundations',
  'ModCast #70: Seeing What There Is To See',
  "ModCast #71: Faucet's On",
  'ModCast #72: Where the Buffalo Roam',
  'ModCast #74: So Much Perfect',
  'PolyCast Play-by-Play #01: Unification',
  'PolyCast Episode 255: That Much More Enticing',
  'PolyCast Episode 256: All About the Hype Train',
  'PolyCast Episode 257: Now Streamlined',
  'PolyCast Episode 258: Is It October Yet?',
  'PolyCast Episode 259: Rock, Paper, Scissors',
  'PolyCast Episode 261: Delineate These Things',
  'PolyCast Episode 262: Variety of Threads',
  'PolyCast Episode 263: Come Back to That',
  'PolyCast Episode 264: Congratulations, Condolences and All the Rest',
  'PolyCast Episode 265: Speaking Of',
  'PolyCast Episode 266: Explode with Information Overload',
  'PolyCast Episode 267: Nerd Out On Anything',
  'PolyCast Episode 268: Just Jump In',
  "PolyCast Episode 269: That's Our Number",
  'PolyCast Christmas Special 2016: We Wish You a Merry Civmas',
  'PolyCast Episode 270: A Step in the Direction',
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
    throw new Error(`Response status: ${response.status}`);
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

  baseChannel.querySelector('title')!.textContent = 'PolyCast and ModCast classic';
  baseChannel.querySelector('description')!.textContent =
    'Classic episodes of PolyCast and ModCast';
  baseChannel
    .getElementsByTagName('itunes:image')[0]
    .setAttribute('href', 'https://polycast.civfanatics.com/images/polycast_logo300.jpg');
  baseChannel.querySelector('pubDate')!.textContent = new Date().toUTCString();
  const imageEl = Array.from(baseChannel.children).find((el) => el.tagName === 'image');
  if (imageEl) {
    imageEl.querySelector('url')!.textContent =
      'https://polycast.civfanatics.com/images/polycast_logo140.jpg';
    imageEl.querySelector('link')!.textContent = 'https://thepolycast.net/';
    imageEl.querySelector('width')!.textContent = '144';
    imageEl.querySelector('height')!.textContent = '91';
  }

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
        continue;
      }

      if (
        title &&
        episodeSubstringsToFilterOut.some((substring) =>
          title.includes(substring)
        )
      ) {
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
    'polycast-classic.xml',
    doc.documentElement.outerHTML.replaceAll('\n', '\r\n')
  );
};

main();
