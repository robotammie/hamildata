// add event listeners to nav bar
$(function(){
  $('#song-connections').click(function (evt) {
      location.hash = ""
      $('#about').empty();
      $('#chart').empty();
      $('#info-box').empty();
    
      setupPage();
  });
});

$(function(){
  $('#search-lyrics').click(function (evt) {
      location.hash = "search"
      $('#about').empty();
      $('#chart').empty();
      $('#info-box').empty();

      setupPage();
  });
});

$(function(){
  $('#about-site').click(function (evt) {
      location.hash = "about"
      $('#about').empty();
      $('#chart').empty();
      $('#info-box').empty();

      setupPage();
  });
});

function setupPage() {
  if (location.hash === "#search") {
    generateBarPage("#chart");
    $('#li-lyrics').toggleClass( 'active', true );
    $('#li-about').toggleClass( 'active', false );
    $('#li-connections').toggleClass( 'active', false );
    }
    else if (location.hash === "#about") {
    generateAbout("#about");
    $('#li-about').toggleClass( 'active', true );
    $('#li-lyrics').toggleClass( 'active', false );
    $('#li-connections').toggleClass( 'active', false );
    }
  else {
    generateBundles("#chart")
    $('#li-connections').toggleClass( 'active', true );
    $('#li-lyrics').toggleClass( 'active', false );
    $('#li-about').toggleClass( 'active', false );
  };
}

setupPage();