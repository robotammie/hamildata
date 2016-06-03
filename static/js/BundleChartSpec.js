describe("Testing network chart functionality", function() {
  
  beforeAll(function(done) {
    // render the chart
    generateBundles('#chart', done);

  });

  // Testing basic chart
  it('should render a chart with minimal requirements', function(){
      expect($('#chart').html()).toContain("svg");
  });

  it("should have song titles as labels", function() {
    expect($('.node')[0].innerHTML).toEqual("Alexander Hamilton");
  });`

});
