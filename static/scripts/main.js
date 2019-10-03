function openTab(tabName) {
  var tabcontent = document.getElementById(tabName);
  var tablink = document.getElementById(tabName.replace("-tab","-link"));
     
  if(tablink.checked){
        tabcontent.className += " active";
  }
  else{
        tabcontent.className = tabcontent.className.replace(" active","");
        var children = tabcontent.children;
        for(var i = 0; i<children.length; i++){
              var child = children[i];
              if(child.type=="text"){
                    child.value="";
              }
              else if(child.type=="select-one"){
                    var options = child.children;
                    child.value = options[0].value;
              }             
        }
  }
}

//save inputed phenotypes in an array to submit
var listPhenotypes = [];

function addPhenotype(event){
   var key = event.which || event.keyCode;
   if (key===13){
      //prevent submission of form
      event.preventDefault();

      var currentInput = event.currentTarget.value;
      if (currentInput.startsWith('HP')&&!listPhenotypes.includes(currentInput)){
         var error = document.getElementById("duplication-error");
         if (error!==null) {error.remove();}
         listPhenotypes.push(currentInput);   //add term to array
         event.currentTarget.value="";  //clear field after adding

         //append added items to webpage
         var parentNode = document.createElement("div");
         var node = document.createElement("div");
         node.setAttribute("class", "selected-phenotype");
         var textnode = document.createTextNode(currentInput);
         node.appendChild(textnode);
         parentNode.appendChild(node);

         //append delete buttons
         var deleteButton = document.createElement("button");
         deleteButton.innerHTML = "Delete";
         deleteButton.type = "button";
         deleteButton.setAttribute("class", "delete-button");
         deleteButton.setAttribute("onclick", "deletePhenotype(this)");
         parentNode.appendChild(deleteButton);

         document.getElementById("phenotype-tab").appendChild(parentNode);
         
       }
       else if (listPhenotypes.includes(currentInput)){
         var node = document.createElement("div");
         node.setAttribute("id", "duplication-error");
         var textnode = document.createTextNode("Duplicated term has already been added.");
         node.appendChild(textnode);
         document.getElementById("phenotype-tab").appendChild(node);
         event.currentTarget.value="";
       }
   }
}

//delete when delete button is pressed
function deletePhenotype(a){
   var ind = listPhenotypes.indexOf(a.parentNode.firstChild.firstChild.nodeValue);
   if (ind > -1){
      listPhenotypes.splice(ind, 1);
   }
   a.parentNode.remove();
}

//when submitting, append the list of selected phenotypes as input
function appendPhenotype(){
    var myForm = document.getElementById('search-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.id = 'existing-list';
    hiddenInput.name = 'phenotype';
    hiddenInput.value = listPhenotypes.toString();
    myForm.appendChild(hiddenInput);   
}
