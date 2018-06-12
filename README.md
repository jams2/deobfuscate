# deobfuscate.py

This script un-mangles Javascript obscured by common techniques.

---

## Usage

`$ python deobfuscate.py -h`

```
usage: deobfuscate.py [-h] [-l | -d <delim> [<delim> ...]] [-x] [-a] [-r <start> <end>] infile [outfile]

positional arguments:
infile                .js file to parse
outfile               destination file, print to STDOUT if not specified.

optional arguments:
    -h, --help            show this help message and exit
    -l, --linebreaks      insert linebreaks after ";", or specify delimiters with -d.
    -d <delim> [<delim> ...], --delimiter <delim> [<delim> ...]
                            space separated list of delimiters to break lines on.
                            characters such as ";" may need to be escaped.
    -x, --hex             parse hex encoded characters to ascii.
    -a, --arrays          substitute array references for declared values
    -r <start> <end>, --range <start> <end>
                            range of lines to parse (non-inclusive). applied before other actions.
```

### Example

`input.js`:

```
var _0x652a=["\x75\x73\x65\x20\x73\x74\x72\x69\x63\x74","\x63\x6C\x61\x73\x73\x4E\x61\x6D\x65","\x66\x69\x72\x73\x74\x45\x6C\x65\x6D\x65\x6E\x74\x43\x68\x69\x6C\x64","\x2E\x6D\x65\x6E\x75\x2D\x69\x74\x65\x6D","\x71\x75\x65\x72\x79\x53\x65\x6C\x65\x63\x74\x6F\x72","\x61\x63\x74\x69\x76\x65","\x2E\x6D\x65\x6E\x75\x2D\x69\x74\x65\x6D\x3E\x61","\x71\x75\x65\x72\x79\x53\x65\x6C\x65\x63\x74\x6F\x72\x41\x6C\x6C","\x23\x6D\x65\x6E\x75\x2D\x68\x65\x61\x64\x65\x72","\x68\x32","\x63\x6C\x69\x63\x6B","\x74\x61\x72\x67\x65\x74","\x61\x64\x64\x45\x76\x65\x6E\x74\x4C\x69\x73\x74\x65\x6E\x65\x72","\x66\x6F\x72\x45\x61\x63\x68","\x73\x63\x72\x6F\x6C\x6C","\x76\x69\x73\x69\x62\x69\x6C\x69\x74\x79","\x73\x74\x79\x6C\x65","\x68\x69\x64\x64\x65\x6E","\x76\x69\x73\x69\x62\x6C\x65","\x73\x63\x72\x6F\x6C\x6C\x59","\x69\x6E\x6E\x65\x72\x48\x65\x69\x67\x68\x74","\x23\x63\x6F\x6E\x74\x61\x63\x74\x2D\x73\x75\x62\x6D\x69\x74","\x6F\x66\x66\x73\x65\x74","\x61\x62\x73","\x6D\x61\x70","\x6D\x69\x6E","\x69\x6E\x64\x65\x78\x4F\x66","\x23","\x69\x64","\x2D\x6C\x69\x6E\x6B"];_0x652a[0];function addListeners(){document[_0x652a[4]](_0x652a[3])[_0x652a[2]][_0x652a[1]]= _0x652a[5];let _0x973cx2=document[_0x652a[7]](_0x652a[6]);let _0x973cx3=document[_0x652a[4]](_0x652a[8]);let _0x973cx4=getDivOffsets(document[_0x652a[7]](_0x652a[9]));var _0x973cx5;_0x973cx2[_0x652a[13]]((_0x973cx6)=>{_0x973cx6[_0x652a[12]](_0x652a[10],(_0x973cx7)=>{highlightOne(_0x973cx2,_0x973cx7[_0x652a[11]]);_0x973cx5= true})});window[_0x652a[12]](_0x652a[14],()=>{if(!_0x973cx5&& _0x973cx3[_0x652a[16]][_0x652a[15]]=== _0x652a[17]){_0x973cx3[_0x652a[16]][_0x652a[15]]= _0x652a[18]};_0x973cx5= false;if(window[_0x652a[19]]% 5=== 0){scrollSpy(_0x973cx4,window[_0x652a[20]],_0x973cx2)}});document[_0x652a[4]](_0x652a[21])[_0x652a[12]](_0x652a[10],handleSubmit)}function scrollSpy(_0x973cx4,_0x973cx9,_0x973cx2){let _0x973cxa=_0x973cx4[_0x652a[24]]((_0x973cxb)=>Math[_0x652a[23]](window[_0x652a[19]]+ (_0x973cx9/ 4)- _0x973cxb[_0x652a[22]]));let _0x973cxc=_0x973cxa[_0x652a[26]](Math[_0x652a[25]](..._0x973cxa));let _0x973cxd=document[_0x652a[4]](_0x652a[27]+ _0x973cx4[_0x973cxc][_0x652a[28]]+ _0x652a[29]);if(_0x973cxd[_0x652a[1]]!== _0x652a[5]){highlightOne(_0x973cx2,_0x973cxd)}}
```


Specifying no options results in all actions being performed by default:

`$ python deobfuscate.py input.js`

```
var _0x652a=["use strict","className","firstElementChild",".menu-item","querySelector","active",".menu-item>a","querySelectorAll","#menu-header","h2","click","target","addEventListener","forEach","scroll","visibility","style","hidden","visible","scrollY","innerHeight","#contact-submit","offset","abs","map","min","indexOf","#","id","-link"];
"use strict";
function addListeners(){document["querySelector"](".menu-item")["firstElementChild"]["className"]= "active";
    let _0x973cx2=document["querySelectorAll"](".menu-item>a");
    let _0x973cx3=document["querySelector"]("#menu-header");
    let _0x973cx4=getDivOffsets(document["querySelectorAll"]("h2"));
    var _0x973cx5;
    _0x973cx2["forEach"]((_0x973cx6)=>{_0x973cx6["addEventListener"]("click",(_0x973cx7)=>{highlightOne(_0x973cx2,_0x973cx7["target"]);
                _0x973cx5= true})});
    window["addEventListener"]("scroll",()=>{if(!_0x973cx5&& _0x973cx3["style"]["visibility"]=== "hidden"){_0x973cx3["style"]["visibility"]= "visible"};
            _0x973cx5= false;
            if(window["scrollY"]% 5=== 0){scrollSpy(_0x973cx4,window["innerHeight"],_0x973cx2)}});
    document["querySelector"]("#contact-submit")["addEventListener"]("click",handleSubmit)}function scrollSpy(_0x973cx4,_0x973cx9,_0x973cx2){let _0x973cxa=_0x973cx4["map"]((_0x973cxb)=>Math["abs"](window["scrollY"]+ (_0x973cx9/ 4)- _0x973cxb["offset"]));
        let _0x973cxc=_0x973cxa["indexOf"](Math["min"](..._0x973cxa));
        let _0x973cxd=document["querySelector"]("#"+ _0x973cx4[_0x973cxc]["id"]+ "-link");
        if(_0x973cxd["className"]!== "active"){highlightOne(_0x973cx2,_0x973cxd)}}
```

---

Specify delimiters for linebreaks, parse hex, don't substitute array array references:

`$ python deobfuscate.py -d \; \, \} -x input.js`

```
var _0x652a=["use strict",
    "className",
    "firstElementChild",
    ".menu-item",
    "querySelector",
    "active",
    ".menu-item>a",
    "querySelectorAll",
    "#menu-header",
    "h2",
    "click",
    "target",
    "addEventListener",
    "forEach",
    "scroll",
    "visibility",
    "style",
    "hidden",
    "visible",
    "scrollY",
    "innerHeight",
    "#contact-submit",
    "offset",
    "abs",
    "map",
    "min",
    "indexOf",
    "#",
    "id",
    "-link"];
_0x652a[0];
function addListeners(){document[_0x652a[4]](_0x652a[3])[_0x652a[2]][_0x652a[1]]= _0x652a[5];
    let _0x973cx2=document[_0x652a[7]](_0x652a[6]);
    let _0x973cx3=document[_0x652a[4]](_0x652a[8]);
    let _0x973cx4=getDivOffsets(document[_0x652a[7]](_0x652a[9]));
    var _0x973cx5;
    _0x973cx2[_0x652a[13]]((_0x973cx6)=>{_0x973cx6[_0x652a[12]](_0x652a[10],
                (_0x973cx7)=>{highlightOne(_0x973cx2,
                        _0x973cx7[_0x652a[11]]);
                _0x973cx5= true}
                )}
            );
    window[_0x652a[12]](_0x652a[14],
            ()=>{if(!_0x973cx5&& _0x973cx3[_0x652a[16]][_0x652a[15]]=== _0x652a[17]){_0x973cx3[_0x652a[16]][_0x652a[15]]= _0x652a[18]}

            ...
```


---

## Setup
### Run tests:

`git clone https://github.com/jams2/deobfuscate.git`

`cd deobfuscate`

`python3 -m venv ./deobfuscate`

`source deobfuscate/bin/activate`

`pip install -r requirements.txt`

`pip install -e .`

`pytest`

`coverage run -m pytest && coverage report`


