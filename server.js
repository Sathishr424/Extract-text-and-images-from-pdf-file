const express     = require('express');
const bodyParser  = require('body-parser');

const fs = require('fs');
const path = require('path');
const multer  = require('multer');

const upload = multer({dest: 'download/'});
const {PythonShell} = require('python-shell');

const app = express();
app.set('json spaces', 2);

const PDFParser = require("pdf2json");

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use('/', express.static(process.cwd() + '/'));

try{
    let py_file = fs.readFileSync(path.join("py_installed"));
}catch (err){
    let py = require("./pythonPackageInstaller.js");
    py.install_python_packages();
}

//Index page (static HTML)

// try{
//     let py_file = fs.readFileSync("py_installed");
// }catch (err){
//     let py = require("./pythonPackageInstaller.js");
//     py.install_python_packages();
// }

app.route('/').get(function (req, res) {
    res.sendFile(__dirname + "/index.html");
});

app.post('/extract_pdf', upload.single('pdf'), (req,res)=>{

    fs.readdir(path.join(__dirname, 'download'), (err, files) => {
      if (err) throw err;

      for (const file of files) {
        console.log('File', file, req.file['filename'])
        if (file != req.file['filename']) fs.unlink(path.join(path.join(__dirname, 'download'), file), err => {
          if (err) throw err;
        });
      }
    });

    var file = req.file;
    console.log(file);

    var retData = {'text':[], 'image':[]};

    var pdfParser = new PDFParser();

    pdfParser.on("pdfParser_dataError", errData => res.send(errData.parserError) );
    pdfParser.on("pdfParser_dataReady", pdfData => {
        // console.log(pdfParser)
        console.log(pdfData['Pages'].length);
        // res.json(pdfData)
        var pages = pdfData['Pages'];

        PythonShell.run(path.join(__dirname, "/src/PDFImageExtraction.py"), {args: [path.join(__dirname, file.path)]}, (err,results) => {
            if (err) throw err;
            else{
                console.log('Results', results); 
                if (results[0] == 'Error extracting image!') {res.send("Failed to extract PDF!");}
                else{
                    // fs.unlinkSync(__dirname + "/" + file.path);
                    pages.map((page, i)=>{
                        page['Texts'].map(text=>{
                            if (text['R'].length > 1) console.log("Warning!!!!!", text['R'])
                            retData['text'].push({'str': decodeURI(text['R'][0]['T']), 'page': i+1, 'x':text['x'], 'y':text['y'], 'width':text['w'], 'height':text['sw']});
                        })
                    });
                    iData = fs.readFileSync(path.join(__dirname, 'src', "imageJson"))
                    console.log(iData)
                    retData['image'] = JSON.parse(iData);
                    // console.log(retData)
                    res.json(retData);
                }
            }
        });
    });

    pdfParser.loadPDF(file.path);
})

const listener = app.listen(process.env.PORT || 4000, function () {
    console.log('Your app is listening on port ' + listener.address().port);
});