// Based on https://stackoverflow.com/a/38543075/399105
function httpsRequest(url) {
  const options = new URL(url);

  return new Promise(function(resolve, reject) {
    let request = https.request(options, async function(response) {
      if (response.statusCode < 200 || response.statusCode >= 300) {
        reject(new Error('statusCode=' + response.statusCode));
      }

      let body = [];
      response.on('data', function(chunk) {
        body.push(chunk);
      });

      response.on('end', function() {
        resolve(Buffer.concat(body).toString());
      });
    });

    request.on('error', function(err) {
      reject(err);
    });

    request.end();
  });
}
