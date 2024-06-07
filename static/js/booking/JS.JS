//function displayText() {
//  document.querySelector('.text').style.display ='block';
//  document.querySelector('.new_booking').style.display='block';
//}
//
//function displayExisting() {
//    document.querySelector('.text').style.display ='none';
//    document.querySelector('.new_booking').style.display='none';
//}
//
//let date_val = new Date();
//let today_date = date_val.getDate();
//let month_val = date_val.getMonth()+1;
//let year_val = date_val.getFullYear();
//
//if (month_val<10) {
//    month_val = "0"+month_val.toString();
//}
//if (today_date<10) {
//    today_date = "0"+today_date.toString();
//}
//let min_date = year_val + '-' + month_val + '-' + today_date;
//document.getElementById("date").setAttribute('min', min_date);
//
//var btnBook = document.querySelectorAll('.btn_book');
//
//btnBook.forEach(button => {
//    button.addEventListener('click', (e) => {
//        btnBook.forEach(button => {
//            book_remove(e,button);
//        });
//        book_add(e, button);
//    });
//});
//
//var book_remove = function (e, button){
//    if (e.target.classList.contains('btn_book')){
//        button.classList.remove('active');
//        if (!button.classList.contains('active')) {
//            document.querySelector('.time_Slots').style.display ='none';
//            document.querySelector('.wrapper').classList.remove('overlay');
//        }
//    }
//};
//
//var book_add = function (e, button) {
//    if (e.target.classList.contains('btn_book')){
//        button.classList.add('active');
//        if (button.classList.contains('active')) {
//            displayTime();
//            document.querySelector('.wrapper').classList.add('overlay');
//        }
//    }
//};
//
//var displayTime = function () {
//
//    document.querySelector('.time_Slots').style.display ='block';
//
//    let id = document.querySelector('.active');
//    let idVal = id.value;
//
//    const aaaa = document.querySelector('.btn_book');
//    console.log(aaaa);
//
//    let doctor_name = document.querySelector(`.doctor_name${idVal}`);
//    let get = doctor_name.value;
//
//    let doctor_specialist = document.querySelector(`.doctor_specialist${idVal}`);
//    let get_spe = doctor_specialist.value;
//    let doctor_img = document.querySelector(`.img${idVal}`).getAttribute('src');
//    let date_get = document.querySelector(`.date${idVal}`);
//    let date_va = date_get.value;
//    let loc = document.querySelector(`.locat${idVal}`);
//   let loc_val = loc.value;
//
//    sessionStorage.setItem('doctor_name', get );
//    sessionStorage.setItem('specialization', get_spe );
//    sessionStorage.setItem('date', date_va );
//    sessionStorage.setItem('Location', loc_val );
//
//
//    let flex_btn = document.querySelector('.flex_btn');
//    let divCreate = `<div class="doctor_data">
//                        <div class="imgdiv">
//                            <img src="${doctor_img}">
//                        </div>
//                        <div>
//                            <p class="doctor">${get}</p>
//                            <p class="doctor_spe">${get_spe}</p>
//                            <p class="date_time">${date_va}</p>
//                        </div>
//                     </div>`;
//    flex_btn.insertAdjacentHTML('beforebegin',divCreate);
//
//
//
//    const timeslot = (fromTime, toTime, slots) => {
//        let time_start = new Date(fromTime).valueOf();
//        let slot = new Date(fromTime).valueOf() + slots * 1000;
//        let time_end = new Date(toTime).valueOf();
//        let time_diff = [];
//
//        for(slot; slot<=time_end; slot= slot+slots*1000) {
//            time_diff.push(
//                {
//                    'from': formatDate(time_start),
//                    'to': formatDate(slot),
//                }
//            );
//            time_start = slot;
//        }
//        return time_diff;
//    };
//
//    const formatDate = (time) => {
//        let d = new Date(time);
//        let month = String((d.getMonth() + 1)).padStart(2, '0');
//        let day = String((d.getDate())).padStart(2, '0');
//        let hours = String((d.getHours())).padStart(2, '0');
//        let min = String((d.getMinutes())).padStart(2, '0');
//        return `${hours}:${min}`;
//    };
//
//    let from_time = document.querySelector(`#from${idVal}`);
//    let to_time = document.querySelector(`#to${idVal}`);
//    let date = document.querySelector('#date');
//    let time1 = from_time.value;
//    let time2 = to_time.value;
//    let dateVal = date.value;
//    const dateTime1 = `${dateVal} ${time1}`;
//    const dateTime2 = `${dateVal} ${time2}`;
//    slots = 30*60;
//
//    const time = timeslot(dateTime1, dateTime2, slots)
//    const time_slot = [];
//
//    for (let {from, to} of time ){
//        time_slot.push(from);
//    }
//
//    let container = document.querySelector('.morning_time');
//    let container_after = document.querySelector('.afternoon_time');
//    let container_evening = document.querySelector('.evening_time');
//
//    let date_compare = new Date(`${dateVal}T12:00:00`);
//    let date_compare1 = new Date(`${dateVal}T16:00:00`);
//    let date_compare2 = new Date(`${dateVal}T21:00:00`);
//    let time_len = time_slot.length;
//    console.log(time_len);
//
//    time_slot.forEach(function(time_str){
//        let act = `${dateVal}`+' '+time_str+`:00`;
//        let actual_time = new Date(act);
//
//        var ii = function input(div) {
//            let input = document.createElement('input');
//            div.classList.add("input");
//            input.type = 'checkbox';
//            input.value = time_str;
//            input.classList.add("input_btn");
//            div.appendChild(input);
//            container_after.appendChild(div);
//        };
//
//        if (actual_time < date_compare){
//            let div = document.createElement('div');
//            ii(div);
//            let label = document.createElement('label');
//            label.innerText = time_str+' AM';
//            div.appendChild(label);
//            container.appendChild(div);
//        }
//
//        else if (actual_time < date_compare1) {
//            let div = document.createElement('div');
//            ii(div);
//            let label = document.createElement('label');
//            label.innerText = time_str+' PM';
//            div.appendChild(label);
//            container_after.appendChild(div);
//        }
//
//        else {
//            let div = document.createElement('div');
//            ii(div);
//            let label = document.createElement('label');
//            label.innerText = time_str+ 'PM';
//            div.appendChild(label);
//            container_evening.appendChild(div);
//        }
//    });
//
//    var data = document.querySelector('.doctor_data');
//    var buttons = document.querySelectorAll('.input_btn');
//    console.log(buttons);
//    buttons.forEach(input => {
//        input.addEventListener('click', () => {
//             buttons.forEach(input => {
//                remove_input(input);
//             });
//            add_input(input);
//        });
//    });
//
//    var remove_input = (input)  => {
//        input.classList.remove('active');
//        var val = document.querySelector('.value');
//        if (val !== null) {
//            val.remove();
//        }
//    };
//
//    var add_input = (input) => {
//        input.classList.add('active');
//        if (input.classList.contains('active')){
//            let create_input= document.createElement('input');
//            create_input.type = 'text';
//            create_input.setAttribute('value', input.value);
//            create_input.setAttribute('hidden', true);
//            create_input.classList.add("value");
//            data.appendChild(create_input);
//            sessionStorage.setItem('from',input.value );
//        }
//    };
//};
//
//const closeTime = document.querySelector('#closed');
//const close_Time = document.querySelector('.btnCancel');
//
//const timeClose = function () {
//    document.querySelector('#time_Slots').style.display='none';
//    document.querySelector('#time_Slots').style.display='none';
//    let d = document.querySelector('.doctor_data');
//    d.remove();
//
//    document.querySelector('.wrapper').classList.remove('overlay');
//    let input = document.querySelectorAll('.input');
//    input.forEach(inputs => {
//        inputs.remove();
//    });
//}
//
//closeTime.addEventListener('click', timeClose);
//close_Time.addEventListener('click', timeClose);
//
//$(document).ready(function(){
//    function handleChange(){
//        var date =  $('.dates').val();
//        var location = $('.loc').val();
//        var department = $('.dept').val();
//
//        $.ajax({
//            type:'POST',
//            url:'/books/',
//            cache: false,
//            data: {
//                date:date,
//                location:location,
//                department:department,
//            },
//            success: function(response) {
//                console.log(typeof response)
//                var data = JSON.stringify(response);
//                data = JSON.parse(data);
//                console.log(data);
//                let html='';
//                data.data.forEach(j => {
//                console.log("j",j.id);
//                    data.user_data.forEach(i => {
//                        if(j.user_id_id == i.id) {
//                            html +=
//                                `<div class="doctor_appointment--book">
//                                    <a href="#" class="doctor_detail--block book${i.id}" onchange="get_data()">
//                                        <div class="doctor_img">
//                                            <img src="/media/${i.img}" class="doctor_imgs img${i.id}"" alt="doctor_img">
//                                        </div>
//                                        <div class="doctor_info">
//                                            <span class="doctor_name" >Dr. ${i.first_name} ${i.last_name} </span>
//                                            <input type="text" id="" class="doctor_name${i.id}" value="Dr. ${i.first_name} ${i.last_name}" hidden="hidden">
//                                            <span class="doctor_specialist">${i.designation}</span>
//                                            <input type="text" id="" class="doctor_specialist${i.id}" value="${i.designation}" hidden="hidden">
//                                            <span class="doctor_Exp">${i.experience}, ${i.education} </span>
//                                            <span class="docotor_location">${j.location}</span>
//                                            <input type="date" id="date" class="datechange" value="${j.date}" hidden="hidden">
//                                            <input type="text" id="date" class="datechange date${i.id}" value="${j.date}" hidden="hidden">
//                                            <input type="text" id="from${i.id}" class="from_time" value="${j.from_time}" hidden="hidden">
//                                            <input type="text" id="to${i.id}" class="to_time" value="${j.to_time}" hidden="hidden">
//                                            <span class="clinic_name">Clinic: </span>
//
//                                        </div>
//                                    </a>
//                                    <div class="book_block">
//                                        <button type="submit" class="btn_book book_btn  btn${i.id}" value="${i.id}" >Book an Appointment</button>
//                                    </div>
//                                </div>`;
//                             }
//                        });
//                    });
//                    document.querySelector('.dcotor_lists').innerHTML = html;
//                    const b = document.querySelectorAll(".btn_book");
//                    b.forEach(button => {
//                        button.addEventListener('click', (e) => {
//                            btnBook.forEach(button => {
//                                book_remove(e,button);
//                            });
//                            book_add(e, button);
//                        });
//                    });
//                }
//            });
//        }
//    $(".dates, .loc, .dept").change(handleChange);
//});


let date_val = new Date();
let today_date = date_val.getDate();
let month_val = date_val.getMonth()+1;
let year_val = date_val.getFullYear();

if (month_val<10) {
    month_val = "0"+month_val.toString();
}
if (today_date<10) {
    today_date = "0"+today_date.toString();
}
let min_date = year_val + '-' + month_val + '-' + today_date;
document.getElementById("date").setAttribute('min', min_date);

var btnBook = document.querySelectorAll('.btn_book');

btnBook.forEach(button => {
    button.addEventListener('click', (e) => {
        btnBook.forEach(button => {
            book_remove(e,button);
        });
        book_add(e, button);
    });
});

let book_remove = function (e, button){
    if (e.target.classList.contains('btn_book')){
        button.classList.remove('active');
        if (!button.classList.contains('active')) {
            document.querySelector('.time_Slots').style.display ='none';
            document.querySelector('.wrapper').classList.remove('overlay');
        }
    }
};

let book_add = function (e, button) {
    if (e.target.classList.contains('btn_book')){
        button.classList.add('active');
        if (button.classList.contains('active')) {
            displayTime();
            document.querySelector('.wrapper').classList.add('overlay');
        }
    }
};

let displayTime = function () {

    document.querySelector('.time_Slots').style.display ='block';

    let id = document.querySelector('.active');
    let idVal = id.value;

    const aaaa = document.querySelector('.btn_book');
    console.log(aaaa);

    let doctor_name = document.querySelector(`.doctor_name${idVal}`);
    let get = doctor_name.value;

    let doctor_specialist = document.querySelector(`.doctor_specialist${idVal}`);
    let get_spe = doctor_specialist.value;
    let doctor_img = document.querySelector(`.img${idVal}`).getAttribute('src');
    let date_get = document.querySelector(`.date${idVal}`);
    let date_va = date_get.value;

    let flex_btn = document.querySelector('.flex_btn');
    let divCreate = `<div class="doctor_data">
                        <div class="imgdiv">
                            <img src="${doctor_img}">
                        </div>
                        <div>
                            <p class="doctor">${get}</p>
                            <p class="doctor_spe">${get_spe}</p>
                            <p class="date_time">${date_va}</p>
                        </div>
                     </div>`;
    flex_btn.insertAdjacentHTML('beforebegin',divCreate);



    const timeslot = (fromTime, toTime, slots) => {
        let time_start = new Date(fromTime).valueOf();
        let slot = new Date(fromTime).valueOf() + slots * 1000;
        let time_end = new Date(toTime).valueOf();
        let time_diff = [];

        for(slot; slot<=time_end; slot= slot+slots*1000) {
            time_diff.push(
                {
                    'from': formatDate(time_start),
                    'to': formatDate(slot),
                }
            );
            time_start = slot;
        }
        return time_diff;
    };

    const formatDate = (time) => {
        let d = new Date(time);
        let month = String((d.getMonth() + 1)).padStart(2, '0');
        let day = String((d.getDate())).padStart(2, '0');
        let hours = String((d.getHours())).padStart(2, '0');
        let min = String((d.getMinutes())).padStart(2, '0');
        return `${hours}:${min}`;
    };

    let from_time = document.querySelector(`#from${idVal}`);
    let to_time = document.querySelector(`#to${idVal}`);
    let date = document.querySelector('#date');
    let time1 = from_time.value;
    let time2 = to_time.value;
    let dateVal = date.value;
    const dateTime1 = `${dateVal} ${time1}`;
    const dateTime2 = `${dateVal} ${time2}`;
    slots = 30*60;

    const time = timeslot(dateTime1, dateTime2, slots)
    const time_slot = [];

    for (let {from, to} of time ){
        time_slot.push(from);
    }

    let container = document.querySelector('.morning_time');
    let container_after = document.querySelector('.afternoon_time');
    let container_evening = document.querySelector('.evening_time');

    let date_compare = new Date(`${dateVal}T12:00:00`);
    let date_compare1 = new Date(`${dateVal}T16:00:00`);
    let date_compare2 = new Date(`${dateVal}T21:00:00`);
    let time_len = time_slot.length;
    console.log(time_len);

    time_slot.forEach(function(time_str){
        let act = `${dateVal}`+' '+time_str+`:00`;
        let actual_time = new Date(act);

        if (actual_time < date_compare){
            let input = document.createElement('input');
            let div = document.createElement('div');
            div.classList.add("input");
            input.type = 'checkbox';
            input.value = time_str;
            input.classList.add("input_btn");
            div.appendChild(input);
            container.appendChild(div);
            let label = document.createElement('label');
            label.innerText = time_str+' AM';
            div.appendChild(label);
            container.appendChild(div);
        }

        else if (actual_time < date_compare1) {
            let input = document.createElement('input');
            let div = document.createElement('div');
            div.classList.add("input");
            input.type = 'checkbox';
            input.value = time_str;
            input.classList.add("input_btn");
            div.appendChild(input);
            container_after.appendChild(div);
            let label = document.createElement('label');
            label.innerText = time_str+' PM';
            div.appendChild(label);
            container_after.appendChild(div);
        }

        else {
            let input = document.createElement('input');
            let div = document.createElement('div');
            div.classList.add("input");
            input.type = 'checkbox';
            input.value = time_str;
            input.classList.add("input_btn");
            div.appendChild(input);
            container_evening.appendChild(div);
            let label = document.createElement('label');
            label.innerText = time_str+ 'PM';
            div.appendChild(label);
            container_evening.appendChild(div);
        }

     });

    var data = document.querySelector('.doctor_data');
    var buttons = document.querySelectorAll('.input_btn');
    console.log(buttons);
    buttons.forEach(input => {
        input.addEventListener('click', () => {
             buttons.forEach(input => {
                remove_input(input);
             });
            add_input(input);
        });
    });

    let remove_input = (input)  => {
        input.classList.remove('active');
        var val = document.querySelector('.value');
        if (val !== null) {
            val.remove();
        }
    };

    let add_input = (input) => {
        input.classList.add('active');
        if (input.classList.contains('active')){
            let create_input= document.createElement('input');
            create_input.type = 'text';
            create_input.setAttribute('value', input.value);
            create_input.setAttribute('hidden', true);
            create_input.classList.add("value");
            data.appendChild(create_input);
        }
    };
};

const closeTime = document.querySelector('#closed');
const close_Time = document.querySelector('.btnCancel');

const timeClose = function () {
    document.querySelector('#time_Slots').style.display='none';
    document.querySelector('#time_Slots').style.display='none';
    let d = document.querySelector('.doctor_data');
    d.remove();

    document.querySelector('.wrapper').classList.remove('overlay');
    let input = document.querySelectorAll('.input');
    input.forEach(inputs => {
        inputs.remove();
    });
}

closeTime.addEventListener('click', timeClose);
close_Time.addEventListener('click', timeClose);

$(document).ready(function(){
    function handleChange(){
        var date =  $('.dates').val();
        var location = $('.loc').val();
        var department = $('.dept').val();

        $.ajax({
            type:'POST',
            url:'/books/',
            cache: false,
            data: {
                date:date,
                location:location,
                department:department,
            },
            success: function(response) {
                console.log(typeof response)
                var data = JSON.stringify(response);
                data = JSON.parse(data);
                console.log(data);
                let html='';
                data.data.forEach(j => {
                console.log("j",j.id);
                    data.user_data.forEach(i => {
                        if(j.user_id_id == i.id) {
                            html +=
                                `<div class="doctor_appointment--book">
                                    <a href="#" class="doctor_detail--block book${i.id}" onchange="get_data()">
                                        <div class="doctor_img">
                                            <img src="/media/${i.img}" class="doctor_imgs img${i.id}"" alt="doctor_img">
                                        </div>
                                        <div class="doctor_info">
                                            <span class="doctor_name" >Dr. ${i.first_name} ${i.last_name} </span>
                                            <input type="text" id="" class="doctor_name${i.id}" value="Dr. ${i.first_name} ${i.last_name}" hidden="hidden">
                                            <span class="doctor_specialist">${i.designation}</span>
                                            <input type="text" id="" class="doctor_specialist${i.id}" value="${i.designation}" hidden="hidden">
                                            <span class="doctor_Exp">${i.experience}, ${i.education} </span>
                                            <span class="docotor_location">${j.location}</span>
                                            <input type="date" id="date" class="datechange" value="${j.date}" hidden="hidden">
                                            <input type="text" id="date" class="datechange date${i.id}" value="${j.date}" hidden="hidden">
                                            <input type="text" id="from${i.id}" class="from_time" value="${j.from_time}" hidden="hidden">
                                            <input type="text" id="to${i.id}" class="to_time" value="${j.to_time}" hidden="hidden">
                                            <span class="clinic_name">Clinic: </span>

                                        </div>
                                    </a>
                                    <div class="book_block">
                                        <button type="submit" class="btn_book book_btn  btn${i.id}" value="${i.id}" >Book an Appointment</button>
                                    </div>
                                </div>`;
                             }
                        });
                    });
                    document.querySelector('.dcotor_lists').innerHTML = html;
                    const b = document.querySelectorAll(".btn_book");
                    b.forEach(button => {
                        button.addEventListener('click', (e) => {
                            btnBook.forEach(button => {
                                book_remove(e,button);
                            });
                            book_add(e, button);
                        });
                    });
                }
            });
        }
    $(".dates, .loc, .dept").change(handleChange);
});