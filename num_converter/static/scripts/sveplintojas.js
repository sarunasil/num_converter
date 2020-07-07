
function sveplinti() {
            var bef = document.getElementById("TextBoxIn").value;
            var after = makeSortString(bef);
            document.getElementById("TextBoxOut").value = after;

            document.getElementById("Label2").textContent = bef.length;
            document.getElementById("Label3").textContent = after.length;
}

function makeSortString(s) {
    if (!makeSortString.translate_re)
        makeSortString.translate_re = /[ĄČĘĖĮŠŲŪŽąčęėįšųūž]/g;
    var translate = {
        "Ą": "A", "Č": "C", "Ę": "E",
        "Ė": "E", "Į": "I", "Š": "S",
        "Ų": "U", "Ū": "U", "Ž": "Z",
        "ą": "a", "č": "c", "ę": "e",
        "ė": "e", "į": "i", "š": "s",
        "ų": "u", "ū": "u", "ž": "z",
    };
    return (s.replace(makeSortString.translate_re, function (match) {
        return translate[match];
    }));
}

function copy() {
    document.getElementById("TextBoxOut").focus();
    document.getElementById("TextBoxOut").select();
}
