let {PythonShell} = require('python-shell');

module.exports.install_python_packages = function(){
	PythonShell.run(__dirname + '/src/package_installer.py', {args: ["pdfminer", "pymupdf"]}, (err,results)=>{
		if (err) throw err;
		else console.log(results);
	});
}
