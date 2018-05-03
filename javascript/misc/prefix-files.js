/*
 * This will add a numerical prefix (e.g. "005 - ") to all of the files in the current folder in random order
 */

const fs = require('fs');

const PREFIX_LENGTH = 3;

function main() {
  let filenames = getFilesInCurrentDirectory();
  filenames = shuffleArray(filenames);
  let prefixLength = getPrefixLength(filenames.length);

  for (let i = 0; i < filenames.length; i++) {
    let oldFilename = filenames[i];
    let prefix = String(filenames.indexOf(oldFilename) + 1).padStart(prefixLength, '0');
    let newFilename = `${prefix} - ${oldFilename}`;

    console.log(`Renaming ${oldFilename} to ${newFilename}`);

    renameFile(oldFilename, newFilename);
  }
}

function getFilesInCurrentDirectory() {
  return fs.readdirSync('.');
}

// https://gist.github.com/guilhermepontes/17ae0cc71fa2b13ea8c20c94c5c35dc4
function shuffleArray(arr) {
  return arr
    .map(a => [Math.random(), a])
    .sort((a, b) => a[0] - b[0])
    .map(a => a[1]);
}

function getPrefixLength(numFilenames) {
  if (typeof PREFIX_LENGTH !== 'undefined' && PREFIX_LENGTH !== null) {
    return PREFIX_LENGTH;
  } else {
    return String(numFilenames + 1).length;
  }
}

function renameFile(oldFilename, newFilename) {
  fs.rename(oldFilename, newFilename, (err) => {
    if (err) throw err;
  });
}

main();
