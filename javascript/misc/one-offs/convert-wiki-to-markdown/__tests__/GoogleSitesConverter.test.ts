import fs from 'fs';
import GoogleSitesConverter from '../GoogleSitesConverter';

test('Convert bold element', () => {
  const htmlString = '<b>Install clamav</b>';
  const expectedMarkdown = '#### Install clamav';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert simple code element', () => {
  const htmlString = '<code>sudo /etc/init.d/clamav-freshclam stop</code>';
  const expectedMarkdown = '```\nsudo /etc/init.d/clamav-freshclam stop\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert code in span element', () => {
  const htmlString = '<span style="color:rgb(0,96,0);font-family:monospace;line-height:1.6;font-size:10pt">sudo update-rc.d clamav-freshclam disable</span>';
  const expectedMarkdown = '```\nsudo update-rc.d clamav-freshclam disable\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert back-to-back code elements', () => {
  const htmlString = '<code>mkdir $HOME/Desktop/infected; sudo clamscan -r --bell -i --move=$HOME/Desktop/infected --exclude-dir=$HOME/Desktop/infected / &amp;&gt; </code><code>$HOME/Desktop/infected</code><code>/scan.txt</code>';
  const expectedMarkdown = '```\nmkdir $HOME/Desktop/infected; sudo clamscan -r --bell -i --move=$HOME/Desktop/infected --exclude-dir=$HOME/Desktop/infected / &> $HOME/Desktop/infected/scan.txt\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert back-to-back code elements, take 2', () => {
  const htmlString = '<div><code>dig SRV _kerberos._udp.example.com</code></div><div><span style="line-height:1.6;font-size:10pt"><code>dig SRV _kpasswd._tcp.example.com</code></span></div><div><div><code>dig SRV _kpasswd._udp.example.com</code></div>';
  const expectedMarkdown = '\n```\ndig SRV _kerberos._udp.example.com\ndig SRV _kpasswd._tcp.example.com\ndig SRV _kpasswd._udp.example.com\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert back-to-back code elements with newline', () => {
  const htmlString = '<code>sudo apt-add-repository ppa:ubuntu-clamav/ppa<br /></code><div><code>sudo apt-get install clamav</code>';
  const expectedMarkdown = '```\nsudo apt-add-repository ppa:ubuntu-clamav/ppa\nsudo apt-get install clamav\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert large bold element', () => {
  const htmlString = '<font size="5"><b>Useful commands</b></font>';
  const expectedMarkdown = '## Useful commands';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert code in italics', () => {
  const htmlString = '<code>cancel </code><i><code>job_name</code></i>';
  const expectedMarkdown = '```\ncancel JOB_NAME\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert italics in code', () => {
  const htmlString = '<code>lp -d <i>printer_name</i> /usr/share/cups/data/testprint.ps</code>';
  const expectedMarkdown = '```\nlp -d PRINTER_NAME /usr/share/cups/data/testprint.ps\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert multiple code in italics elements', () => {
  const htmlString = '<code>lp -d </code><i><code>printer_name</code></i> <i><code>filename</code></i>';
  const expectedMarkdown = '```\nlp -d PRINTER_NAME FILENAME\n```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert indented code', () => {
  const htmlString = '<ul><li><span style="line-height:1.6;font-size:10pt;background-color:transparent">RHEL 5:<br /></span><span style="line-height:1.6;font-size:10pt;background-color:transparent"><code>lp -d <i>printer_name</i> /usr/share/cups/data/testprint.ps</code><br /><br /></span></li></ul>';
  const expectedMarkdown = '\n- RHEL 5:\n    ```\n    lp -d PRINTER_NAME /usr/share/cups/data/testprint.ps\n    ```\n\n';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert indented code with italics', () => {
  const htmlString = '<ul><li>create the principal for the machine/service<br /><code>ank [-policy </code><i><code>policy_name</code></i><code>] -randkey host/</code><i><code>FQDN</code></i></li></ul>';
  const expectedMarkdown = '\n- create the principal for the machine/service\n    ```\n    ank [-policy POLICY_NAME] -randkey host/FQDN\n    ```';
  const convertedMarkdown = GoogleSitesConverter.convertElementsFromString(htmlString);

  expect(convertedMarkdown).toBe(expectedMarkdown);
});

test('Convert page with code', async () => {
  let markdownFromFile = fs.readFileSync('./__tests__/resources/clamav.md').toString('utf8');
  let convertedMarkdown = await GoogleSitesConverter.convertPageFromFile('./__tests__/resources/clamav.html');
  expect(convertedMarkdown).toBe(markdownFromFile);
});

test('Convert page with code in a list', async () => {
  let markdownFromFile = fs.readFileSync('./__tests__/resources/cups.md').toString('utf8');
  let convertedMarkdown = await GoogleSitesConverter.convertPageFromFile('./__tests__/resources/cups.html');
  expect(convertedMarkdown).toBe(markdownFromFile);
});
