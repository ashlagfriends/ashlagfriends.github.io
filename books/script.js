fs = require('fs')
fs.readFile('info.json', 'utf8', function (err,data) {
for (i = 0; i < fs.length; i++) {

  console.log(fs[i])
  }
});
