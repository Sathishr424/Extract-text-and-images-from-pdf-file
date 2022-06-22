const fs = require('fs');
const path = require('path');
const {PythonShell} = require('python-shell');

try{
    let py_file = fs.readFileSync(path.join("py_installed"));
}catch (err){
    let py = require("./pythonPackageInstaller.js");
    py.install_python_packages();
}

async function extractPDF(filePath){

    var retData = {'text':[], 'image':[]};

    return new Promise( async function (resolve){
        PythonShell.run(path.join(__dirname, "/src/PDF_Extraction.py"), {args: [path.join(filePath)]}, (err,results) => {
            if (err) throw err;
            else{
                // console.log('Python ouput', results); 
                if (results[0] == 'Error extracting image!' || results[0] == 'Error extracting text!') {console.log("Failed to extract PDF!");}
                else{
                    console.log(JSON.stringify(results[0]))
                }
            }
        });
    })
}

var ret = []
process.argv.forEach(async function (val, index, array) {
  // console.log(index + ': ' + val);
  if (index > 1){
    var data = await extractPDF(val);
  }
});
