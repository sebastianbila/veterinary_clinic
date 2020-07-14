function onSelectService(e) {
    e.preventDefault();

    let form_url = $('.form-service').attr("action");
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();
    let service_id = $('#select').val();
    let table = $('.table-body');


    $.ajax({
        type: 'POST',
        url: form_url,
        data: {
            'service_id': service_id,
            csrfmiddlewaretoken: csrf_token
        },
        success: function (context) {
            table.empty();

            /* Fill table */
            context['category_services'].forEach(i => {
                console.log(i['title'] === "");
                let template = `
                    <tr>
                        <td>${i['title']}</td>
                        <td>${i['price']}</td>
                    </tr>
                `;
                table.append(template);
            });

            /* If list is empty */
            if (context['category_services'].length === 0) {
                let template = `
                    <tr>
                        <td>Ничего не найдено</td>
                        <td></td>
                    </tr>
                `;
                table.append(template);
            }
        }
    });
}

function deletePatient() {
    let patient_id = $('.patient-id').val();
    console.log(`Deleting patient (${patient_id})`);
    let csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        type: 'POST',
        url: 'delete_patient/',
        data: {
            'id': patient_id,
            csrfmiddlewaretoken: csrf_token
        },
        success: function (context) {
            console.log('Was successfully delete');
            location.reload();
        }
    });

}

function saveRecipe(e) {
    e.preventDefault();
    let recipe_text = $('#recipe_content').val();

    console.log(recipe_text);
    $.ajax({
        type: 'POST',
        url: 'recipe',
        data: {
            'recipe-content': recipe_text,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (context) {
            if (context['status'] === true){
                $('#btnSaveRecipe').hide();
                const element = document.getElementById('recipe');
                html2pdf()
                    .from(element)
                    .save();

                setTimeout(function () {
                    location.reload();
                }, 1500);
            }
        }
    });
}
