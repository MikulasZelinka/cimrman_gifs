
const gifsJson = JSON.parse(gifsData);

var app = new Vue({
  el: '#app',
  data: {
    gifs: gifsJson
  }
})