"use strict";

const MIN_SIMILARITY = 0.81;
const MEDIA_URL = 'https://media.githubusercontent.com/media/araffin/guess-comixify-movie/master/';
const N_MOVIES = 10;
const BASE_POSTER_URL = 'https://image.tmdb.org/t/p/w300_and_h450_bestv2/';
const BASE_MOVIE_DB = 'https://www.themoviedb.org/movie/';
const MIN_DELAY = 200; // ms between answer check
let lang = 'en';

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
  let percent = document.getElementById('percent');
  let results_card = document.getElementById('results');
  let lang_block = document.getElementById('lang-select-block');
  let lang_buttons = document.getElementById('languages');
  let current_idx = -1;
  let movies, results, disObjForm;
  let desintegrated = false;
  let game_over = false;
  let timer, start_time;

  function placeholderMovieInfos() {
      movie_title.textContent = "???";
      movie_more_button.href = '#';
      hide(movie_more_button);
      let placeholder = 'poster.jpg'
      if (base_url.startsWith('https://araffin.github.io'))
      {
        placeholder = MEDIA_URL + placeholder;
      }
      movie_poster.src = placeholder;
  }

  function addMovieInfos() {
    movie_title.textContent = movies[current_idx].names[lang];
    movie_more_button.href = BASE_MOVIE_DB + movies[current_idx].id;
    show(movie_more_button);
    movie_poster.src = BASE_POSTER_URL + movies[current_idx].posters[lang];
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
    show(next_button.parentElement);
  }

  function checkGameOver()
  {
    if (!game_over) {
      game_over = true;
      for (let i = 0; i < results.length; i++)
      {
        if (typeof results[i] == 'undefined')
        {
          game_over = false;
          break;
        }
      }
    }
    return game_over
  }

  function showResults()
  {
    let html = '';
    for (let i = 0; i < movies.length; i++) {
      let success = results[i] == 1;
      let class_ = success ?  'text-success' : 'text-error';
      html += `<p class=${class_}>${i + 1}. ${movies[i].names[lang]}</p>`
    }
    let card_body = results_card.querySelector('.card-body');
    card_body.innerHTML = html;

    let n_success = results.reduce((pv, cv) => pv + cv, 0);
    let n_movies = movies.length;
    results_card.querySelector('.card-subtitle').textContent = `${n_success} / ${n_movies}`;

    show(results_card);
  }

  function updateScore() {
    let n_success = results.reduce((pv, cv) => pv + cv, 0);
    let n_movies = movies.length;
    score.textContent = `${n_success} / ${n_movies}`;
    let n_dones = 0;
    for (let i = 0; i < results.length; i++) {
      if (typeof results[i] != 'undefined') {
        n_dones++;
      }
    }
    percent.textContent = Math.round(100 * n_dones / movies.length);
    percent.parentElement.style.width = percent.textContent  + '%';
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
    placeholderMovieInfos();

    if (checkGameOver())
    {
      hide(image);
      hide(movie_infos);
      hide(dis_elem);
      hide(next_button.parentElement);
      clearInterval(timer);
      updateScore();
      showResults();
      return false;
    }

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
    return true;
  }

  title_input.addEventListener('keyup', _.debounce(function(e){
    let guess = title_input.value.toLowerCase();

    if (guess.length < 1) {
      return;
    }

    let successful_trial = false;
    resetState();

    let langs = Object.keys(movies[current_idx].names);
    langs.forEach(function(lang_key) {
      let name = movies[current_idx].names[lang_key];
      let similarity = compareTwoStrings(guess, name.toLowerCase());
      if (similarity > MIN_SIMILARITY)
      {
        success();
        successful_trial = true;
        return;
      }

    });

    if (!successful_trial) {
      failure();
    }

  }, MIN_DELAY));

  pass_button.addEventListener('click', function(e){
    resetState();
    addToFailedMovies();
    nextMovie();
  });

  next_button.addEventListener('click', function(e){
    resetState();
    if (nextMovie())
    {
      hide(next.parentElement);
      show(dis_elem);
    }
  });

  reveal.addEventListener('click', function(e){
    disintegrateBlock();
    addMovieInfos();
    addToFailedMovies();
  });

  refresh.addEventListener('click', function(e){
      location.reload();
  });

  languages.addEventListener('click', function(e){
    lang = e.target.value;
    hide(lang_block);
    title_input.focus();
    start_time = new Date().getTime();
    startTimer();
  });

  loadJSON(function(response) {
    // Parse JSON string into object
    movies = JSON.parse(response).movies;
    movies = _.shuffle(movies);
    movies = _.take(movies, N_MOVIES);
    results = new Array(movies.length);
    nextMovie();
  });


  function startTimer()
  {
    // Update the timer every 1 second
    timer = setInterval(function() {

      // Get todays date and time
      let now = new Date().getTime();

      // Find the distance between now and the count down date
      let distance = now - start_time;

      // Time calculations for days, hours, minutes and seconds
      let days = Math.floor(distance / (1000 * 60 * 60 * 24));
      let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      let seconds = Math.floor((distance % (1000 * 60)) / 1000);

      if (hours   < 10) {hours   = "0" + hours;}
      if (minutes < 10) {minutes = "0" + minutes;}
      if (seconds < 10) {seconds = "0" + seconds;}

      document.getElementById("timer").innerHTML = `${minutes} : ${seconds}`;

      // document.getElementById("timer").innerHTML = days + "d " + hours + "h "
      // + minutes + "m " + seconds + "s ";

    }, 1000);

  }

});
