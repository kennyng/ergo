// edit/add meds page - show textbox if other option is selected
// bad coding style... ><
$( '#meds-edit' ).live( 'pageinit',function(event){
   // Document is ready
   $('#select-med').change(function(){
    console.log("change");
      if ($(this).val() == "Other"){
        $('.other-text').show();
      }
      else {
        $('.other-text').hide();
      }
    });
});
  
$( '#allergies-edit' ).live( 'pageinit',function(event){
   // Document is ready
   $('#select-med').change(function(){
    console.log("change");
      if ($(this).val() == "Other"){
        $('.other-text').show();
      }
      else {
        $('.other-text').hide();
      }
    });
});

  //TODO: add dynamically created items
  /*
    <div class="one-shelf">
      <div class="shelf-item" id="zyrtec">
        <div>Zyrtec</div>
        <div><img src="../static_files/images/zyrtec.jpg" /></div>
      </div>
      ....
    </div>
    //create the above divs
    var shelfDiv = document.createElement('div'); //alternative append("<div></div>").. jquery
    //add class "one-shelf"
    shelfDiv.className = "one-shelf";
    //add class
    var itemDiv = document.createElement('div');
    itemDiv.className = "shelf-item";
    var medDiv = document.createElement('div');
    medDiv.text( .... json text ... );
    var imgDiv = document.createElement('div');
    var img = document.createElement('img');
    img.src = ... json img name ...
    itemDiv.append(medDiv);
    itemDiv.append(imgDiv);
    $('.shelf').append(shelfDiv);
  */
$( '#prescription' ).live( 'pageinit',function(event){ 
  console.log("pre onload");
  addOnClick("#popupDialog");
});

$( '#otc' ).live( 'pageinit',function(event){ 
console.log("otc onload");
  addOnClick("#popupDialog-otc");
});


$( '#misc' ).live( 'pageinit',function(event){ 
  addOnClick("#popupDialog-misc");
});


function addOnClick(popid){
  var shelves;
  if (popid == "#popupDialog"){
    shelves = $('.prescription > div.one-shelf');
  }
  else if (popid == "#popupDialog-otc"){
    shelves = $(' .otc > div.one-shelf');
  }
  else {
    shelves = $('.misc > div.one-shelf');
  }
  console.log(shelves);
  //access each single shelf
  shelves.each(function() { 
    // add popup onclick to each shelf item
    $(this).children().each(function(){
      if ($(this).data("clicked") == ("false")){  
        $(this).hide();
      }
      this.onclick = function(){
        $(popid).popup("open");
        $(this).data("clicked", "true");
        console.log($(this).data("clicked"));
        console.log("p id: ", popid);
      };
    });
  });  
  
  $('.status-msg').hide(); //default no status msg, only show upon delete 
}
 
function deleteClicked(){
  var deleted;
   $('.one-shelf').each(function() { 
    // add popup onclick to each shelf item
    $(this).children().each(function(index){
      if ($(this).data("clicked") == ("true")){
        $(this).fadeOut("slow");
        $(this).data("clicked", "false");
        deleted = this.id;
        document.deleteForm.action = "/drugs/remove?drug_id=" + this.id;
        console.log(index, document.deleteForm);
        // since all same form, can use any of the forms to submit the delete request?
        //document.deleteForm[0].submit(); 
        return;
      }
    });
  });
  $('.status-msg').text("Successfully deleted " + capitaliseFirstLetter(deleted) + ".");
  //$('.status-msg').show();
  $('.status-msg').slideDown(1000);
  window.setTimeout(function(){
    $('.status-msg').slideUp(1000);
  },5000);
  
}

function cancelClicked(){
  $('.one-shelf').each(function() { 
    // add popup onclick to each shelf item
    $(this).children().each(function(index){
      if ($(this).data("clicked") == ("true")){
        $(this).removeData("clicked");
        return;
      }
    });
  });
}

function capitaliseFirstLetter(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}
/*$("ul.jcarousel-skin-tango li").click(function(){
  //console.log(this);
    $("li").each(function (index, liElem){
        $(liElem).data("clicked","false");
     })
     console.log($(this));
     $(this).data("clicked", "true");
   });*/
  
  // Set all carousel li elements' borders to inactive
  /*$('#' + id).each(function (index, li) {
    $(li).css("border", "1px solid rgba(0, 0, 0, .1)");
    $(li).data("clicked","false");
    console.log($(index), $(li));
  });
  // Set clicked element border to active
  this.style.border = "2px solid #B3B3B3";
  $(li).data("clicked","true");
  console.log(this.id);
   window.location.href = "/meds-edit.html";
 
function deleteClickedLi(){
   $("li").each(function (index, liElem){
      if ($(liElem).data("clicked") == ("true")){
        $(liElem).hide();
        console.log($(index), $(liElem));
        return;
      }
   })
}*/


// Create items for the jCarousel of annual SLA review hit/misses
function create_carousel_items(id) {
    /* HTML example skeleton
    <li data-clicked="false">
      <a href="#popupDialog" data-rel="popup" data-position-to="window" data-inline="true" data-transition="pop">
        <div><img src="../static_files/images/medicine.png" /></div>
        <div>Xanax</div>
      </a>
    </li>
    */
    // Create list element of date and semicircle icons
    
    var data = null;/*= {{ drugs_json| safe}}; */
    var category;
    if (id == "pre-carousel"){
      category = "prescription";
    }
    else if (id == "otc-carousel"){
      category = "otc";
    }
    else {
      category = "misc";
    }
    var drugNames = data[category].drug_name;
    var drugImages = data[category].drug_img; // assuming images are in same order as names
    
    // for each drug in the json, create an li for the carousel
    for (var i = 0; i < drugNames.length; i++){
      
      var li = document.createElement('li');
      li.id = name;

      // change border upon click, re-route to edits page
      li.onclick = function(){
        // Set all carousel li elements' borders to inactive
        $('#' + id).each(function (index, li) {
          $(li).css("border", "1px solid rgba(0, 0, 0, .1)");
          $(li).data("clicked","false");
          console.log($(index), $(li));
        });
        // Set clicked element border to active
        this.style.border = "2px solid #B3B3B3";
        $(li).data("clicked","true");
        console.log(this.id);
         window.location.href = "/meds-edit.html";
      };

      //<a href="#popupDialog" data-rel="popup" data-position-to="window" data-inline="true" data-transition="pop">
      var a = document.createElement('a');
      a.data("rel", "popup");
      a.data("position-to", "window");
      a.data("inline", "true");
      a.data("transition","pop");
      a.onclick= "liOnClick(this.id)";
      a.href = "#popupDialog";
      
      // Add drug image 
      var imgDiv = document.createElement('div');
      var img = document.createElement('img');
      img.src = drugImages[i];
      a.appendChild(imgDiv);
      
      // Add drug name
      var nameDiv = document.createElement('div');
      nameDiv.innerText = name;
      a.appendChild(nameDiv);

      li.appendChild(a);
      
      // Add new list item to carousel ul
      $("#" + id).append(li); // Assumes given in abc order
    }
  }
 