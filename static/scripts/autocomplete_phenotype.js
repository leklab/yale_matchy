var phenotypes;

jQuery.ajax({
        url:'http://yale-matchy.org:5000/static/hpo_terms.txt', 
        success: function(data) {
            phenotypes = data.split("\n");
        }, 
        async:false});


var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substringRegex;
  
      // an array that will be populated with substring matches
      matches = [];
  
      // regex used to determine if a string contains the substring `q`
      substrRegex = new RegExp(q, 'i');
  
      // iterate through the pool of strings and for any string that
      // contains the substring `q`, add it to the `matches` array
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push(str);
        }
      });
  
      cb(matches);
    };
};
  
  $('#phenotype').typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'phenotypes',
    source: substringMatcher(phenotypes),
    limit: 8
  });



//phenotype okay idk how this works
/*
var phenotypeSuggest = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: 'http://10.5.33.255:5000/scripts/hpo_terms.txt',
    //wildcard: '%QUERY'
  }
});

$('#phenotype').typeahead({
  hint: true,
  highlight: true,
  minLength: 3
},
{
  name: 'phenotypes',
  source: phenotypeSuggest
});
*/
