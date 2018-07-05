'use strict';

const https = require('https');
const jsdom = require('jsdom');
const {JSDOM} = jsdom;
const {URL} = require('url');

// TODO: remove this
const util = require('util');

// const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/clamav';
const WIKI_URL = 'https://sites.google.com/site/bmaupinwiki/home/applications/misc/cups';

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

  let markdown = convertPageTitle(pageTitle) + convertContent(contentElement);

  markdown = cleanupMarkdown(markdown);

  console.log(markdown);


  // contentElement.
}

function convertPageTitle(title) {
  return `---\ntitle: ${title}\n---\n`;
}

function convertContent(contentElement) {
  // console.log(contentElement.innerHTML);

  let markdown = '';

  for (let i = 0; i < contentElement.childNodes.length; i++) {
    let childElement = contentElement.childNodes[i];

    markdown += convertElement(childElement);

    if (childElement.hasChildNodes()) {
      markdown += convertContent(childElement);
    }
  }

  return markdown;
}

function convertElement(htmlElement) {
  switch(htmlElement.tagName) {
    case 'B':
      return `\n\n#### ${htmlElement.textContent}\n`;

    case 'CODE':
      return `\`\`\`\n${htmlElement.textContent}\n\`\`\`\n`;

    case 'BR':
      return '';

    case 'LI':
      if (htmlElement.parentNode.tagName === 'UL') {
        return '- ';
      }

    case 'SPAN':
      if (htmlElement.getAttribute('style').includes('font-family:monospace')) {
        return `\`\`\`\n${htmlElement.textContent}\n\`\`\`\n`;
      } else {
        return `${htmlElement.textContent}\n`;
      }

    case 'DIV':
      // This should handle divs that only contain text
      if (htmlElement.children.length === 0 && htmlElement.childNodes.length !== 0) {
        return `${htmlElement.textContent}\n`;
      } else {
        return '';
      }

    default:
      console.error(`WARNING: HTML element not handled: ${htmlElement.outerHTML}`);
      return '';
  }
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

main();
