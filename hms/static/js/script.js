var a = document.getElementById('togglePassword');
var p = document.getElementById('password');
console.log(p);

a.addEventListener('click', function (e) {
   const type = p.getAttribute('type') === 'password' ? 'text' : 'password';
   p.setAttribute('type', type);
   this.classList.toggle('fa-eye-slash');
});



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


let email = document.querySelector('#mail');
let error = document.querySelector('#errors');

email.addEventListener('input', function(e) {
    let val = e.target.value;
    console.log(val);
    const emailRegex = /^\w+([\.-]?\w+)*(\@\w{5,10})+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (emailRegex.test(val)) {
        error.textContent ="";
    }
    else {
        error.textContent = "Please Enter Valid Email";
    }
});



let ab = document.querySelector('#phonenumber');
let bc = document.querySelector('#err');

ab.addEventListener('input', function(e) {
    let c = e.target.value;
    console.log(c);
    const verify = /^\+?[1-9]\d{11,20}$/;
    if (verify.test(c)) {
        bc.textContent ="";
    }
    else {
        bc.textContent = "Please Enter Valid Phone Number ex: +91914*******";
    }
});