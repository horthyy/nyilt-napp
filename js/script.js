/* FELADATOK:
 * ablakméret (@media cucc)
 * checkbox
 * szerverre küldés felhasználói adatokkal
 * fejléc, lábléc
 */



const TANTARGYAK_SZAMA = 31;
const IDOREND_START = {
    "0": 430,
    "1": 490,
    "2": 545,
    "3": 605,
    "4": 660,
    "5": 715,
    "6": 770,
    "7": 840,
    "8": 890,
    "9": 960, 
}; // IDOREND_END[i] = IDOREND_START[i] + 45

var cardNagyitas = true; // card nagyítás animáció toggle

function timeConvert(ido) {
    ido = ido.split(":");
    return parseInt(ido[0])*60 + parseInt(ido[1]);
};


//idő alapú keresés (AZ EREDMÉNY FORDÍTVA VAN, AZ IF-ELSE RÉSZNÉL NEGÁLNI KELL)
function compareStart(per, start) {
    if (start > IDOREND_START[per]) {
        return false;
    } else {
        return true;
    };
};
function compareEnd(per, end) {
    if (IDOREND_START[per]+45 > end) {
        return false;
    } else {
        return true;
    };
};


// KÁRTYA ANIMÁCIÓ
var mouseOverCheckbox = false;
function boxFocus(bool) {
    if (bool) {
        mouseOverCheckbox = true;
    } else {
        mouseOverCheckbox = false;
    }
}

function toggleCard(inputCard) {
    if (mouseOverCheckbox) {
        return; //ha a kurzor egy checkboxon van, nem csukja össze a cardot
    }

    var obj = inputCard;
    if (obj.style.height == '320px') {
        obj.style.height = '126px';

        if (cardNagyitas) {
            obj.style.width = '40%';
        }

    } else {
        obj.style.height = '320px';

        if (cardNagyitas) {
            obj.style.width = '60%';
        }
    }
}

function getClassString(group) {
    if (typeof group == 'string') {
        return '<b>osztály: </b>' + group;
    } else {
        let out = '<b>osztályok: </b>';
        for (i=0;i<group.length;i++) {
            out += group[i] + ', '
        }
        out = out.slice(0, -2); // leszedi a végéről a ', ' részt
        return out;
    }
}

function showSearchResults(n) {
    if (n==0) {
        document.getElementById("searchResults").innerHTML = '<p id="result">Nincs találat a keresésre :(</p>';
    } else {
        document.getElementById("searchResults").innerHTML = '<p id="result">' + n + ' találat a keresésre.</p>';
    };
};


var cards = document.getElementsByClassName("card");

function filterCards() {  //sima keresés
    // KERESŐ MEZŐ:
    var searchValue = document.getElementById("search");
    var searchFor = searchValue.value.toUpperCase();
    // TANTÁRGY SELECT:
    var searchSubjectMenu = document.getElementById("subjectSearch");
    var subjectSearchFor = searchSubjectMenu.options[searchSubjectMenu.selectedIndex].value;
    // IDŐPONT SELECT:
    var timeSearchStart = document.getElementById("timeOption-start").value;
    var timeSearchEnd = document.getElementById("timeOption-end").value;

    var filter, period;
    var resultCount = 0;

    for (i=0;i<cards.length;i++) {
        filter = cards[i].outerHTML.toUpperCase();
        filter = filter.replaceAll(".",""); // '...'
        period = cards[i].getAttribute("data-period");

        if (filter.indexOf(subjectSearchFor.toUpperCase()) == -1) {
            cards[i].style.display = "none";
            //a tantárgy egyezik-e
            resultCount += 1;

        } else if (!compareStart(period, timeConvert(timeSearchStart) )) {
            cards[i].style.display = "none";
            //a kezdési idő megfelelő-e
            resultCount += 1;

        } else if (!compareEnd(period, timeConvert(timeSearchEnd) )) {
            cards[i].style.display = "none";
            //a végződési idő megfelelő-e
            resultCount += 1;

        } else if (filter.indexOf(searchFor) == -1) {
            cards[i].style.display = "none";
            //a keresési mező ellenőrzése 
            resultCount += 1;

        } else {
            cards[i].style.display = "";
            //ha minden teszten átment akkor marad 
        };
    };
    showSearchResults(cards.length - resultCount);
};

function resetSearch() {
    document.getElementById('subjectSearch').value = "";
    document.getElementById('timeOption-start').value = "";
    document.getElementById('timeOption-end').value = "";
    document.getElementById('search').value = "";
}

//  ----  DEPREKÁLT ----
function filterSubjects() { //tantárgy dropdown select keresés
    var filter;

    for (i=0;i<cards.length;i++) {
        filter = cards[i].outerHTML.toUpperCase();
        if (filter.indexOf(subjectSearchFor.toUpperCase()) > -1) {
            cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
    }
}

var selectedStack = 0; // számláló, hogy mennyi van kiválasztva. A submit gomb megjelenítéséhez kell
function selectLesson(selectedBox) {
    let lessonId = selectedBox.getAttribute('id');
    let currentCard = document.getElementById('card-' + lessonId);
    if (selectedBox.checked) {
        currentCard.style.border = "6px solid blue"; // MÁSIK SZÍN !!!!!
        selectedStack++;
    } else {
        currentCard.style.border = "2px solid black";
        selectedStack--;
    }
    
    var submitButton = document.getElementById('submitButton');
    if (selectedStack > 0) {
        submitButton.disabled = false;
        submitButton.removeAttribute("title");
    } else {
        submitButton.disabled = true;
        submitButton.setAttribute("title","Nincsenek kiválasztott órák");
    }
}

function submitLessons() {
    console.log("--- SUBMIT ---")
    document.getElementsByTagName("html")[0].style.pointerEvents = "none";
    var selected_lessons = []; //ez fog átmenni a szerverre
    let submitData = document.getElementsByClassName("selectBox");
    console.log(submitData.length);
    for (i=0;i<submitData.length;i++) {
        if (submitData[i].checked) {
            selected_lessons.push(submitData[i].getAttribute('id'));
        }
    }

    // SUBMIT INFO:
    console.log('Kiválasztott óra id-k:'); // EZT MAJD TÖRÖLNI
    console.log(selected_lessons); // EZT MAJD TÖRÖLNI
}

function filterSelected() {
    if (document.getElementById("filterSelectedBox").checked) {
        for (i=0;i<cards.length;i++) {
            let temp = cards[i].id.toString().split('-')[1];
            if (document.getElementById(temp).checked) {
                cards[i].style.display = "";
            } else {
                cards[i].style.display = "none";
            }
        }
    } else {
        for (i=0;i<cards.length;i++) {
            cards[i].style.display = "";
        }
    }
    
}