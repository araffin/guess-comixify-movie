"use strict";

const MIN_SIMILARITY = 0.81;
const MEDIA_URL = 'https://media.githubusercontent.com/media/araffin/guess-comixify-movie/master/';

disintegrate.init();

let get_url = window.location;
let base_url = get_url .protocol + "//" + get_url.host + "/" + get_url.pathname.split('/')[1];

function ready(fn) {
  if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}


// from https://codepen.io/KryptoniteDove/post/load-json-file-locally-using-pure-javascript
function loadJSON(callback) {

  let xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', 'data.json', true);
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
      // Required use of an anonymous callback as .open
      // will NOT return a value but simply returns undefined in asynchronous mode
      callback(xobj.responseText);
    }
  };
  xobj.send(null);
}


ready(function ()
{
  let try_again = document.getElementById('try-again');
  let reveal = document.getElementById('reveal');
  let title_input = document.getElementById('movie-title');
  let form_group = document.getElementById('movie-input-group');
  let image = document.getElementById('movie-pic');
  let next_button = document.getElementById('next');
  let pass_button = document.getElementById('pass');
  let score = document.getElementById('score');
  let dis_elem = document.getElementById('dis-obj');
  let success_msg = document.getElementById('success-msg');
  let movie_infos = document.querySelector('.movie-infos');
  let movie_title = movie_infos.querySelector('.card-title');
  let movie_more_button = movie_infos.querySelector('.card-body a');
  let movie_poster = movie_infos.querySelector('.card-image img');
  let current_idx = -1;
  let movies, results, disObjForm;
  let desintegrated = false;

  function addMovieInfos() {
    let base_url = 'https://www.themoviedb.org/movie/';
    movie_title.textContent = movies[current_idx].names[0];
    movie_more_button.href = base_url + movies[current_idx].id;
    movie_poster.src = movies[current_idx].poster;
  }

  if(document.querySelector('[data-dis-type="simultaneous"]')) {
    window.addEventListener("disesLoaded", function()
    {
      // Get the relevant Disintegrate object
      disObjForm = disintegrate.getDisObj(dis_elem);
    });
  }

  function disintegrateBlock()
  {
    disintegrate.createSimultaneousParticles(disObjForm);
    hide(dis_elem);
    show(next_button.parentElement)
  }


  function updateScore() {
    let n_success = results.reduce((pv, cv) => pv + cv, 0);
    let n_movies = movies.length;
    score.textContent = `${n_success} / ${n_movies}`;
  }

  function hide(el){
    if (!el.classList.contains('d-hide'))
    {
      el.classList.add('d-hide');
    }
  }

  function show(el){
    if (el.classList.contains('d-hide'))
    {
      el.classList.remove('d-hide');
    }
  }

  function fadeOut(el){
    if (!el.classList.contains('hide'))
    {
      el.classList.add('hide');
    }
  }

  function fadeIn(el){
    if (el.classList.contains('hide'))
    {
      el.classList.remove('hide');
    }
  }

  function resetState() {
    if (form_group.classList.contains('has-error'))
    {
      form_group.classList.remove('has-error');
    }
    if (form_group.classList.contains('has-success'))
    {
      form_group.classList.remove('has-success');
    }
    hide(try_again);
  }

  function addToFailedMovies()
  {

    if (typeof results[current_idx] == 'undefined')
    {
      results[current_idx] = 0;
    }
  }

  function success()
  {
    if (!form_group.classList.contains('has-success'))
    {
      form_group.classList.add('has-success');
    }
    if (typeof results[current_idx] == 'undefined')
    {
      results[current_idx] = 1;
    }
    disintegrateBlock();
    show(success_msg);
    addMovieInfos();
    fadeIn(movie_infos);
    updateScore();
  }

  function failure() {
    if (!form_group.classList.contains('has-error'))
    {
      form_group.classList.add('has-error');
    }
    show(try_again);
  }

  function nextMovie()
  {
    hide(success_msg);
    fadeOut(movie_infos);

    title_input.value = '';
    current_idx += 1;
    if (current_idx >= movies.length) {
        current_idx = 0;
    }
    let image_src = movies[current_idx].image;
    if (base_url.startsWith('https://araffin.github.io'))
    {
      image_src = MEDIA_URL + image_src;
    }
    updateScore();
    image.src = image_src;
  }

  title_input.addEventListener('keyup', _.debounce(function(e){
    let guess = title_input.value.toLowerCase();

    if (guess.length < 1) {
      return;
    }

    let successful_trial = false;
    resetState();
    for (let i = 0; i < movies[current_idx].names.length; i++)
    {
      let name = movies[current_idx].names[i];
      let similarity = compareTwoStrings(guess, name.toLowerCase());
      if (similarity > MIN_SIMILARITY)
      {
        success();
        successful_trial = true;
        break;
      }
    }

    if (!successful_trial) {
      failure();
    }

  }, 350));

  pass_button.addEventListener('click', function(e){
    resetState();
    addToFailedMovies();
    nextMovie();
  });

  next_button.addEventListener('click', function(e){
    resetState();
    nextMovie();
    hide(next.parentElement);
    show(dis_elem);
  });

  reveal.addEventListener('click', function(e){
    disintegrateBlock();
    addMovieInfos();
    fadeIn(movie_infos);
    addToFailedMovies();
  });

  loadJSON(function(response) {
    // Parse JSON string into object
    movies = JSON.parse(response).movies;
    movies = _.shuffle(movies);
    results = new Array(movies.length);
    nextMovie();
    title_input.focus();
  });

});
