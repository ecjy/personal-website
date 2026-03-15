const mammoth = require("mammoth");
const fs = require("fs");
const path = require("path");

const docPath = path.join(__dirname, "TPM 2025 Eddie Chong.docx");

mammoth.extractRawText({path: docPath})
    .then(function(result){
        const text = result.value;
        fs.writeFileSync(path.join(__dirname, "extracted_resume.txt"), text);
        console.log("Extraction complete. Text saved to extracted_resume.txt");
    })
    .catch(function(err){
        console.error(err);
    });
