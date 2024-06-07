var a = document.getElementById('togglePassword');
var p = document.getElementById('password');
console.log(p);

a.addEventListener('click', function (e) {
   const type = p.getAttribute('type') === 'password' ? 'text' : 'password';
   p.setAttribute('type', type);
   this.classList.toggle('fa-eye-slash');
});


function toggeleNavBar(element) {
    // console.log(element);


   var sidebar = document.getElementById('sidebar-section');
   var items = sidebar.querySelectorAll('.sidebar_lists');
   items.forEach(function(item) {
       item.classList.remove('active');
    //    console.log("remove");
   });

   element.classList.add('active');
};



function toggleSubMenu(element) {
   var submenuItems = element.parentElement.querySelectorAll('.sub-lists');
   submenuItems.forEach(function(item) {
       item.classList.remove('active');
   });
   element.classList.add('active');
}


function myFunction() {
   document.getElementById("myDropdown").classList.toggle("show");
 }

window.onclick = function(event) {
   if (!event.target.matches('.profile_btn')) {
       var dropdowns = document.getElementById("myDropdown");
       var i;
       for (i = 0; i < dropdowns.length; i++) {
           var openDropdown = dropdowns[i];
           if (openDropdown.classList.contains('show')) {
               openDropdown.classList.remove('show');
           }
       }
   }
}


function searchFilter() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("search");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (var i = 1; i < tr.length; i++) {
      var tds = tr[i].getElementsByTagName("td");
      var flag = false;
      for(var j = 0; j < tds.length; j++){
        var td = tds[j];
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          flag = true;
        }
      }
      if(flag){
          tr[i].style.display = "";
      }
      else {
          tr[i].style.display = "none";
      }
    }
  }