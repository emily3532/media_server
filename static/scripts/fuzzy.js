
try{
  document.getElementById("finder").addEventListener('keyup', onKeydown);


}
catch(err){
}
try{
  document.getElementById("findertv").addEventListener('keyup', tvdown);
}
catch(err){

}

try{
    document.getElementById("findermovie").addEventListener('keyup', moviedown);
}
catch(err){

}

function moviedown(e) {
  console.log("moviedown")
  if(!e.target.value) { return; }

  console.log(e.target.value);
  str = "?searchterm=" + e.target.value
  console.log(str)

      fetch('/search/fuzzy_search_movies'+str)
    .then(function (response) {
        return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
      outputSearchResults(json)
    })
}
function tvdown(e) {
  console.log("tvdown")
  if(!e.target.value) { return; }

  console.log(e.target.value);
  str = "?searchterm=" + e.target.value
  console.log(str)


      fetch('/search/fuzzy_search_shows'+str)
    .then(function (response) {
        return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
      outputSearchResults(json)
    })

}
function onKeydown(e) {
  console.log("printing")
  if(!e.target.value) { return; }
  var formaction = getsearchtarget()
  console.log(formaction)
  console.log(e.target.value);
  str = "?searchterm=" + e.target.value
  console.log(str)
  if(formaction == '/search/movie') {
      fetch('/search/fuzzy_search_movies'+str)
    .then(function (response) {
        return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
      outputSearchResults(json)
    })
  }
    else if(formaction == '/search/tvshow') {
      fetch('/search/fuzzy_search_shows'+str)
    .then(function (response) {
        return response.json(); // But parse it as JSON this time
    })
    .then(function (json) {
        console.log('GET response as JSON:');
        console.log(json); // Here’s our JSON object
      outputSearchResults(json)
    })
  }
}
function getsearchtarget()
{
    //Get the select select list and store in a variable
    var k = document.getElementById("searchtarget");
    if(!k.options[k.selectedIndex].value) { return; }
    //Get the selected value of the select list
    var formaction = k.options[k.selectedIndex].value;
    console.log(formaction)
    //Update the form action
    document.searchform.action = formaction;
    return formaction;
}

function outputSearchResults(results) {
  // clear list
  document.getElementById("myDropdown").innerHTML='';

  outputMatches(results);
  document.getElementById("myDropdown").classList.toggle("show");
}

function outputMatches(json){
  json.forEach((match) => {
    var a = document.createElement('a');
    if(match['movie_id']){
      rf = '/movie/' + match['movie_id']
      a.href = rf
      a.innerHTML = match['movie_title']
    }
    else{
      rf = '/tvshow/' + match['tvshow_id']
      a.href = rf
      a.innerHTML = match['tvshow_title']
    }
    document.getElementById("myDropdown").insertAdjacentElement('afterbegin', a)
  })
  console.log(document.getElementById("myDropdown").innerHTML)
}

// window.onclick = function(event) {
//   if (!event.target.matches('.dropbtn')) {
//     var dropdowns = document.getElementsByClassName("dropdown-content");
//     var i;
//     for (i = 0; i < dropdowns.length; i++) {
//       var openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains('show')) {
//         openDropdown.classList.remove('show');
//       }
//     }
//   }
// }

