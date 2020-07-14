/* Hide the alert through specific time */
$(".alert").fadeTo(2000, 500).fadeOut(500, function () {
    $(".alert").fadeOut(1000);
});

/**
 * If file was selected in profile
 * @param event
 */
function onFileSelected(event) {
    let btnUpload = document.getElementById("btn-upload-image");
    let selectedFile = event.target.files[0];
    let reader = new FileReader();

    let imgtag = document.getElementById("profile-image");
    imgtag.title = selectedFile.name;

    reader.onload = function (event) {
        imgtag.src = event.target.result;
    };

    reader.readAsDataURL(selectedFile);

    btnUpload.style.display = "inline-block";
    console.log("showing button")
}

/**
 * Click on image to select file
 */
function onImageClick() {
    let input = document.getElementById("selected-image");
    input.click();
}

/**
 * In file was changed
 */
function onFileChange() {
    let selectedFile = event.target.files[0];
    $('#file-name').text(selectedFile.name);
}

/**
 * Fill modal data when click on patient
 * @param patient_id
 */
function openModal(patient_id) {
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    $('#patientModal').modal('show').fadeIn();

    $.ajax({
        type: 'POST',
        url: 'get_patient',
        data: {
            'patient_id': patient_id,
            csrfmiddlewaretoken: csrf_token
        },
        success: function (context) {
            console.log(context);
            let patient = context['patient'];
            let patient_id = $('.patient-id');
            let patient_name = $('#patientName');
            let patient_photo = $('#patientPhoto');
            let patient_description = $('#patientDescription');
            let patient_owner = $('#patientOwner');
            let patient_type = $('#patientType');

            patient_id.val(patient.id);
            patient_photo.attr('src', patient.image);
            patient_name.val(patient.name);
            patient_description.val(patient.description);
            patient_owner.val(patient.owner);
            patient_type.val(patient.type);
        },
    });
}

// If patient photo was selected
function isSelectedPatientPhoto(event) {
    let selectedFile = event.target.files[0];
    let reader = new FileReader();

    let imgtag = document.getElementById("patientPhoto");
    imgtag.title = selectedFile.name;

    reader.onload = function (event) {
        imgtag.src = event.target.result;
    };

    reader.readAsDataURL(selectedFile);
}

let full_price = 0;
$('#endPrice').text(`$${full_price}`);

// Create a new list item when clicking on the "Add" button
function newElement() {
    let service = $('#serviceSelect option:selected');
    let service_id = service.attr('value');
    let service_name = service.attr('label');
    let service_price = service.attr('data-price');

    let li = document.createElement("li");
    li.setAttribute('data-id', service_id);
    li.setAttribute('data-price', service_price);
    li.setAttribute('data-name', service_name);
    li.textContent = service_name + '\xa0';
    li.className = 'list-group-item';
    document.getElementById("listServices").appendChild(li);

    let close_span = document.createElement("SPAN");
    let close_txt = document.createTextNode("\u00D7");
    close_span.className = "close";
    close_span.appendChild(close_txt);
    close_span.addEventListener("click", function () {
        let div = this.parentElement;
        div.parentNode.removeChild(div);
        updateSum();
    });
    li.appendChild(close_span);

    let price_span = document.createElement("SPAN");
    let price_txt = document.createTextNode(`($${service_price})`);
    price_span.className = "text-info price";
    price_span.appendChild(price_txt);
    li.appendChild(price_span);

    updateSum();

    $('#patient').text($('#selectedPatient option:selected').attr('label'));
    $('#owner').text($('#selectedPatient option:selected').attr('data-owner'));
}

//Update sum of all selected services
function updateSum() {
    full_price = 0;
    const listItems = document.querySelectorAll('#listServices li');
    for (let i = 0; i < listItems.length; i++) {
        full_price += parseInt(listItems[i].getAttribute('data-price'));
    }
    $('#endPrice').text(`$${full_price}`);
}

//Save receipt
function saveReceipt(e) {
    console.log('Saving receipt');
    const listItems = document.querySelectorAll('#listServices li');
    let list_services = [];
    for (let i = 0; i < listItems.length; i++) {
        console.log();
        let price = listItems[i].getAttribute('data-price');
        let service = (listItems[i].getAttribute('data-name')) + `(${price})`;
        list_services.push(service);
    }

    let patient = $('#selectedPatient option:selected');
    let patient_name = patient.attr('label');
    console.log(patient_name);

    if (list_services.length !== 0) {
        callAjax(full_price, patient_name, list_services);
    } else {
        alert('Выберите услуги');
    }

}

function callAjax(price, patient, list_services) {
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        type: 'POST',
        url: '',
        data: {
            'full_price': price,
            'patient': patient,
            'services': JSON.stringify(list_services),
            csrfmiddlewaretoken: csrf_token
        },
        success: function (context) {
            $('#btnSave').hide();
            const element = document.getElementById('cardInvoice');
            html2pdf()
                .from(element)
                .save();

            setTimeout(function () {
                location.reload();
            }, 1500);

        }
    });
}


