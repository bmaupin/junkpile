import { JSDOM } from 'jsdom';

declare global {
  interface String {
    replaceAll(search: string, replacement: string): string;
  }
}

String.prototype.replaceAll = function(search: string, replacement: string): string {
  var target = this;
  return target.split(search).join(replacement);
};

export default class GoogleSitesConverter {
  static convertElementsFromString(htmlString: string): string {
    htmlString = `<span>${htmlString}</span>`;
    const htmlElement = JSDOM.fragment(htmlString).firstChild as HTMLElement;
    return GoogleSitesConverter.convertElement(htmlElement, '');
  }

  static async convertPageFromFile(filename: string): Promise<string> {
    let dom = await JSDOM.fromFile(filename);
    return GoogleSitesConverter.convertPage(dom);
  }

  static async convertPageFromUrl(url: string): Promise<string> {
    let dom = await JSDOM.fromURL(url);
    return GoogleSitesConverter.convertPage(dom);
  }

  private static convertPage(dom: JSDOM): string {
    let pageTitle = dom.window.document.getElementById('sites-page-title').textContent;

    let contentParentElements = dom.window.document.getElementsByClassName('sites-layout-tile sites-tile-name-content-1');
    if (contentParentElements.length !== 1) {
      throw new Error('More than one content parent element found');
    }
    if (contentParentElements[0].children.length !== 1) {
      throw new Error('More than one content element found');
    }

    let contentElement = contentParentElements[0].children[0] as HTMLElement;

    let markdown = GoogleSitesConverter.convertPageTitle(pageTitle);
    markdown = GoogleSitesConverter.convertElement(contentElement, markdown);

    if (!markdown.endsWith('\n')) {
      markdown += '\n';
    }

    return markdown;
  }

  private static convertPageTitle(title: string): string {
    return `---\ntitle: ${title}\n---\n\n`;
  }

  private static convertElement(htmlElement: HTMLElement, markdown: string): string {
    const parentNode = htmlElement.parentNode as HTMLElement;
    const grandparentNode = parentNode.parentNode as HTMLElement;

    if (htmlElement.nodeType === 3) {
      const textContent = GoogleSitesConverter.replaceUnwantedCharacters(htmlElement.textContent);

      if ((parentNode.tagName === 'CODE' && grandparentNode.tagName === 'I') ||
        (parentNode.tagName === 'I' && grandparentNode.tagName === 'CODE')) {
        markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + textContent.toUpperCase();
      } else {
        markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + textContent;
      }
    } else {
      switch(htmlElement.tagName) {
        case 'A':
          markdown += '[';
          break;

        case 'B':
          if (!markdown.endsWith('## ')) {
            markdown += `#### `;
          }
          break;

        case 'CODE':
          markdown = GoogleSitesConverter.addMarkdownPrefixForCode(htmlElement, markdown);
          break;

        case 'FONT':
          if (htmlElement.getAttribute('size') === '5') {
            if (markdown.endsWith('#### ')) {
              markdown = markdown.slice(0, -5);
            }
            markdown += `## `;
          }
          break;

        case 'I':
          if (htmlElement.firstChild.nodeType === 3 && parentNode.tagName !== 'CODE') {
            markdown += '*';
            break;
          }
          GoogleSitesConverter.unhandledHtmlElement(htmlElement);
          // markdown += '*';
          break;

        case 'LI':
          if (!markdown.endsWith('\n')) {
            markdown += '\n';
          }
          if (parentNode.tagName === 'OL') {
            markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + '1. ';
            break;
          } else if (parentNode.tagName === 'UL') {
            markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + '- ';
            break;
          }
          GoogleSitesConverter.unhandledHtmlElement(htmlElement);
          break;

        case 'SPAN':
          if (htmlElement.attributes.hasOwnProperty('style') && htmlElement.getAttribute('style').includes('font-family:monospace')) {
            markdown = GoogleSitesConverter.addMarkdownPrefixForCode(htmlElement, markdown);
          } else {
            markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown);
          }
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
          GoogleSitesConverter.unhandledHtmlElement(htmlElement);
          break;
      }
    }

    if (htmlElement.hasChildNodes()) {
      markdown = GoogleSitesConverter.convertChildElements(htmlElement, markdown);
    }

    switch(htmlElement.tagName) {
      case 'A':
        markdown += `](${htmlElement.getAttribute('href')})`;
        break;

      case 'CODE':
        markdown = GoogleSitesConverter.addMarkdownSuffixForCode(htmlElement, markdown);
        break;

      case 'I':
        // Only italicize text nodes for simplicity
        if (htmlElement.firstChild.nodeType === 3 && parentNode.tagName !== 'CODE') {
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
        if (htmlElement.attributes.hasOwnProperty('style') && htmlElement.getAttribute('style').includes('font-family:monospace')) {
          markdown = GoogleSitesConverter.addMarkdownSuffixForCode(htmlElement, markdown);
        }
        break;
    }

    return markdown;
  }

  private static convertChildElements(htmlElement: HTMLElement, markdown: string): string {
    for (let i = 0; i < htmlElement.childNodes.length; i++) {
      let childElement = htmlElement.childNodes[i] as HTMLElement;

      markdown = GoogleSitesConverter.convertElement(childElement, markdown);
    }

    return markdown;
  }

  private static getListItemPadding(htmlElement: HTMLElement, markdown: string): string {
    // Safeguard to make sure we don't add padding in the middle of a line
    if (markdown.endsWith('\n')) {
      // Subtract 1 because we don't want to indent the top level
      let indentDepth = GoogleSitesConverter.getListItemDepth(htmlElement) - 1;

      // A negative indentDepth will cause .repeat to throw an error
      if (indentDepth > 0) {
        return '    '.repeat(indentDepth);
      }
    }

    return '';
  }

  private static getListItemDepth(htmlElement: HTMLElement): number {
    let parentNode = htmlElement.parentNode as HTMLElement;

    if (typeof parentNode !== 'undefined' && parentNode !== null && typeof parentNode.tagName !== 'undefined' &&
      (parentNode.tagName === 'LI' || parentNode.tagName === 'OL' ||
      parentNode.tagName === 'UL')) {
      return GoogleSitesConverter.getListItemDepth(parentNode) + 1;
    } else if (typeof parentNode !== 'undefined' && parentNode !== null) {
      return GoogleSitesConverter.getListItemDepth(parentNode);
    } else {
      return 0;
    }
  }

  private static addMarkdownPrefixForCode(htmlElement: HTMLElement, markdown: string): string {
    // TODO: this needs to be improved to make all tests pass and be simpler if possible
    // markdown = markdown.replace(/\n *$/, '\n');

    if (/\s*?```\s*?$/.test(markdown)) {
      // markdown = markdown.trim();
      // if (markdown.endsWith('```')) {
      //   markdown = markdown.slice(0, -3);
      // }
      // if (markdown.endsWith('\n')) {
      //   markdown = markdown.slice(0, -1);
      // }

      markdown = markdown.replace(/( *?)\n *?```( *?)\n?$/, '$1$2');

      // markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + '```\n';

    // if (markdown.endsWith('\n```')) {
    //   markdown = markdown.slice(0, -4);
    // } else if (markdown.endsWith('\n```\n')) {
    //   markdown = markdown.slice(0, -5);
    } else {
      markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + '```\n';
    }

    return markdown;
  }

  private static addMarkdownSuffixForCode(htmlElement: HTMLElement, markdown: string): string {
    // The newline must be added before calling getListItemPadding. Yes, this is terrible and brittle. But at least it's isolated.
    markdown += '\n';
    markdown += GoogleSitesConverter.getListItemPadding(htmlElement, markdown) + '```';

    return markdown;
  }

  private static unhandledHtmlElement(htmlElement: Element): void {
    console.log(`WARNING: HTML element not handled: ${htmlElement.outerHTML}`);
  }

  private static replaceUnwantedCharacters(stringWithoutReplacements: string): string {
    let stringWithReplacements = stringWithoutReplacements;
    let charsToReplace = {
      // Zero-width space
      '\u200b': '',
      // Non-breaking space
      '\u00a0': ' ',
    };

    for (let charToReplace in charsToReplace) {
      // http://stackoverflow.com/a/1144788/399105
      let regex = new RegExp(charToReplace, 'g');
      stringWithReplacements = stringWithReplacements.replace(regex, charsToReplace[charToReplace]);
    }

    return stringWithReplacements;
  }
}
