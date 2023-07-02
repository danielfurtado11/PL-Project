var express = require('express');
var router = express.Router();
const {spawn} = require('child_process'); 
var fs = require('fs')

/*                                  GET                                       */

/* GET home page. */
router.get('/', function(req, res, next) {
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  res.render('index', {d: data});
});

/* Conversor para JSON */
router.get('/paraJSON', function(req, res, next) {
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  res.render('json', { d: data, erros: undefined});
});

/* Conversor para YAML */
router.get('/paraYAML', function(req, res, next) {
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  res.render('yaml', { d: data, erros: undefined});
});

/* Conversor para XML */
router.get('/paraXML', function(req, res, next) {
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  res.render('xml', { d: data, erros: undefined});
});

/*                                   POST                                      */
// JSON
router.post('/convertJSON', function(req, res){
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  fs.writeFileSync( 'input.toml', req.body.toml)
  fs.renameSync('input.toml', './public/scripts/input.toml')

  var json
  // spawn new child process to call the python script
  console.log(__dirname + '/../public/scripts/anaSinTOML.py')
  const python = spawn('python', ['./public/scripts/anaSinTOML.py', './public/scripts/input.toml', 'JSON']);

  var erros = undefined
  // Captura de erros
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    erros = data.toString();
    console.log(erros)
  });

  python.on('close', (code) => {
   console.log(`child process close all stdio with code ${code}`);
   json = fs.readFileSync("./out.json").toString();
   // send data to browser
   console.log(json)
   res.render('json', {toml: req.body.toml, json: json, d: data, erros: erros})
  });
})

// YAML
router.post('/convertYAML', function(req, res){
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  fs.writeFileSync('input.toml', req.body.toml)
  fs.renameSync('input.toml', './public/scripts/input.toml')

  var yaml
  const python = spawn('python', ['./public/scripts/anaSinTOML.py', './public/scripts/input.toml', 'YAML']);

  var erros = undefined
  // Captura de erros
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    erros = data.toString();
    console.log(erros)
  });

  python.on('close', (code) => {
   console.log(`child process close all stdio with code ${code}`);
   yaml = fs.readFileSync("./out.yaml").toString();
   // send data to browser
   console.log(yaml)
   res.render('yaml', {toml: req.body.toml, yaml: yaml, d: data, erros: erros})
  });
})

// XML
router.post('/convertXML', function(req, res){
  var data = new Date().toISOString().slice(0, 19).split('T').join(' ')
  fs.writeFileSync('input.toml', req.body.toml)
  fs.renameSync('input.toml', './public/scripts/input.toml')

  var xml
  const python = spawn('python', ['./public/scripts/anaSinTOML.py', './public/scripts/input.toml', 'XML']);

  var erros = undefined
  // Captura de erros
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    erros = data.toString();
    console.log(erros)
  });

  python.on('close', (code) => {
   console.log(`child process close all stdio with code ${code}`);
   xml = fs.readFileSync("./out.xml").toString();
   // send data to browser
   console.log(xml)
   res.render('xml', {toml: req.body.toml, xml: xml, d: data, erros: erros})
  });
})

module.exports = router;
