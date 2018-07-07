'use strict';

import https = require('https');
import { JSDOM } from 'jsdom';
import { URL } from 'url';

// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/clamav';
const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/cups';
// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/firefox';

declare global {
  interface String {
    replaceAll(search: string, replacement: string): string;
  }
}

async function main() {
  let dom = await JSDOM.fromURL(WIKI_URL);

  let pageTitle = dom.window.document.getElementById('sites-page-title').textContent;

  let contentParentElements = dom.window.document.getElementsByClassName('sites-layout-tile sites-tile-name-content-1');
  if (contentParentElements.length !== 1) {
    throw new Error('More than one content parent element found');
  }
  if (contentParentElements[0].children.length !== 1) {
    throw new Error('More than one content element found');
  }

  let contentElement = contentParentElements[0].children[0];

  let markdown = convertPageTitle(pageTitle);
  markdown = convertElement(contentElement, markdown);

  console.log(markdown);
}

function convertPageTitle(title) {
  return `---\ntitle: ${title}\n---\n\n`;
}

function convertElement(htmlElement, markdown) {
  if (htmlElement.nodeType === 3) {
    markdown += htmlElement.textContent;
  } else {
    switch(htmlElement.tagName) {
      case 'B':
        if (!markdown.endsWith('## ')) {
          markdown += `#### `;
        }
        break;

      case 'CODE':
        if (markdown.endsWith('\n```')) {
          markdown = markdown.slice(0, -4);
        } else if (markdown.endsWith('\n```\n')) {
          markdown = markdown.slice(0, -5);
        } else {
          markdown += `\`\`\`\n`;
        }
        break;

      case 'FONT':
        // console.log(`FONT: ${htmlElement.getAttribute('size')}`);
        if (htmlElement.getAttribute('size') === '5') {
          if (markdown.endsWith('#### ')) {
            markdown = markdown.slice(0, -5);
          }
          markdown += `## `;
        }
        break;

      case 'I':
        // if (htmlElement.parentNode.tagName !== 'CODE' && htmlElement.firstChild.tagName !== 'CODE') {
        if (htmlElement.firstChild.nodeType === 3) {
          markdown += '*';
          break;
        }
        unhandledHtmlElement(htmlElement);
        // markdown += '*';
        break;

      case 'LI':
        if (htmlElement.parentNode.tagName === 'OL') {
          markdown += getListItemPadding(htmlElement, markdown) + '1. ';
          break;
        } else if (htmlElement.parentNode.tagName === 'UL') {
          markdown += getListItemPadding(htmlElement, markdown) + '- ';
          break;
        }
        unhandledHtmlElement(htmlElement);
        break;

      case 'SPAN':
        if (htmlElement.getAttribute('style').includes('font-family:monospace')) {
          if (markdown.endsWith('\n```')) {
            markdown = markdown.slice(0, -4);
          } else if (markdown.endsWith('\n```\n')) {
            markdown = markdown.slice(0, -5);
          } else {
            markdown += `\`\`\`\n`;
          }
          break;
        }
        // unhandledHtmlElement(htmlElement);
        break;

      case 'DIV':
      case 'OL':
      case 'UL':
        if (!markdown.endsWith('\n')) {
          markdown += '\n';
        }
        break;

      case 'BR':
        markdown += '\n';
        break;

      default:
        unhandledHtmlElement(htmlElement);
        break;
    }
  }

  if (htmlElement.hasChildNodes()) {
    markdown = convertChildElements(htmlElement, markdown);
  }

  switch(htmlElement.tagName) {
    case 'CODE':
      markdown += `\n\`\`\``;
      break;

    case 'I':
      // Only italicize text nodes for simplicity
      if (htmlElement.firstChild.nodeType === 3) {
        // If there's a newline before the end italic, swap them
        if (markdown.endsWith('\n\n')) {
          markdown = markdown.slice(0, -2) + '*' + '\n\n';
        } else if (markdown.endsWith('\n')) {
          markdown = markdown.slice(0, -1) + '*' + '\n';
        } else {
          markdown += '*';
        }
      }
      break;

    case 'SPAN':
      if (htmlElement.getAttribute('style').includes('font-family:monospace')) {
        markdown += `\n\`\`\``;
      }
      break;
  }

  return markdown;
}

function convertChildElements(htmlElement, markdown) {
  for (let i = 0; i < htmlElement.childNodes.length; i++) {
    let childElement = htmlElement.childNodes[i];

    markdown = convertElement(childElement, markdown);
  }

  return markdown;
}

function getListItemPadding(htmlElement, markdown) {
  // Safeguard to make sure we don't add padding in the middle of a line
  if (markdown.endsWith('\n')) {
    // Subtract 1 because we don't want to indent the top level
    let indentDepth = getListItemDepth(htmlElement) - 1;

    // A negative indentDepth will cause .repeat to throw an error
    if (indentDepth > 0) {
      return '    '.repeat(indentDepth);
    }
  }

  return '';
}

function getListItemDepth(htmlElement) {
  if (typeof(htmlElement.parentNode) !== 'undefined' && typeof(htmlElement.parentNode.tagName) !== 'undefined' &&
    (htmlElement.parentNode.tagName === 'LI' || htmlElement.parentNode.tagName === 'OL' ||
    htmlElement.parentNode.tagName === 'UL')) {
    return getListItemDepth(htmlElement.parentNode) + 1;
  } else {
    return 0;
  }
}

function unhandledHtmlElement(htmlElement) {
  console.error(`WARNING: HTML element not handled: ${htmlElement.outerHTML}`);
  return '';
}

function cleanupMarkdown(markdown) {
  // markdown = markdown.replace('```\n```\n', '');
  markdown = markdown.replaceAll('```\n```\n', '');
  return markdown;
}

String.prototype.replaceAll = function(search, replacement) {
  var target = this;
  return target.split(search).join(replacement);
};

// // Based on https://stackoverflow.com/a/38543075/399105
// function httpsRequest(url) {
//   const options = new URL(url);

//   return new Promise(function(resolve, reject) {
//     let request = https.request(options, async function(response) {
//       if (response.statusCode < 200 || response.statusCode >= 300) {
//         reject(new Error('statusCode=' + response.statusCode));
//       }

//       let body = [];
//       response.on('data', function(chunk) {
//         body.push(chunk);
//       });

//       response.on('end', function() {
//         resolve(Buffer.concat(body).toString());
//       });
//     });

//     request.on('error', function(err) {
//       reject(err);
//     });

//     request.end();
//   });
// }

// https://stackoverflow.com/a/43994999/399105
process.on('unhandledRejection', (reason, p) => {
  console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
});

main();
