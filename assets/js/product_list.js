$(document).ready(function () {
    dtable = $('.datatb').DataTable({
        "language": ru_local,
        ajax: {
            url: '/api/product/?format=datatables',
        },
        "columns": [
            {"title": "Наименование", "data": "name"},
            {"title": "Ед. изм.", "data": "unit.name"},
            {"title": "Продукт", "data": "dish.name"},
            {"title": "Вес, кг.", "data": "weight"},
        ],
        "createdRow": function (row, data, dataIndex) {
            row.firstChild.onclick = function () {
                modal_form_show(data, 'Редактировать', 'edit');
            }
        }
    });
});


async function modal_form_show(modal_data, title, modal_type) {
    Swal.fire({
        title: title,
        html:
            '<div class = "form-group">' +
            '   <div class="form-row">' +
            '       <label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Название:</label>' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <input name="input_name" type="text" class="form-control form-control-sm" style="border-color:#AAAAAA;">' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <div name="name-error-msg" style="display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div>' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Ед. изм:</label>' +
            '   </div>' +
            '   <div class="form-row" style="margin-bottom:5px;">' +
            '       <select class="select-unit js-example-basic-single"></select>' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Продукт:</label>' +
            '   </div>' +
            '   <div class="form-row" style="margin-bottom:5px;">' +
            '       <select class="select-dish js-example-basic-single"></select>' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Вес, кг:</label>' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <input name="weight" class="form-control form-control-sm" type="number" step="any" style="border-color:#AAAAAA;"/>' +
            '   </div>' +
            '   <div class="form-row">' +
            '       <div name="weight-error-msg" style="display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div>' +
            '   </div>' +
            '</div>',
        confirmButtonText: 'Подтвердить',
        cancelButtonText: 'Отменить',
        buttonsStyling: true,
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        background: "rgb(255,255,255)",
        preConfirm: async function () {
            $('div[name="name-error-msg"]').text('');
            $('div[name="weight-error-msg"]').text('');

            let ajax_data = {
                unit: $('.select-unit').val(),
                dish: $('.select-dish').val(),
                name: $('input[name="input_name"]').val(),
                weight: $('input[name="weight"]').val()
            };

            if (modal_type == "create")
                res = await modal_create_is_confirm(ajax_data);
            else if (modal_type == "edit")
                res = await modal_edit_is_confirm(modal_data, ajax_data);

            if (res.status == "done") {
                Swal.fire({
                    title: "Успешно",
                    icon: "success"
                });

                if (modal_type == "create")
                    dtable.row.add(res.data).draw();
            } else if (res.status == "failed" && res.data.indexOf("UNIQUE") != -1) {
                $('div[name="name-error-msg"]').text('Это поле должно быть уникальным')
            } else {
                if (res.hasOwnProperty('name')) {
                    $('div[name="name-error-msg"]').text('Это поле не может быть пустым')
                }
                if (res.hasOwnProperty('weight')) {
                    $('div[name="weight-error-msg"]').text('Это поле не может быть пустым')
                }
            }

            return false;
        },
        onOpen: function () {

            $('.select-unit').select2({
                width: '100%',
                ajax: {
                    url: '/api/select2/unit/',
                    dataType: 'json'
                }
            });
            $('.select-dish').select2({
                width: '100%',
                ajax: {
                    url: '/api/select2/dish/?format=json',
                    dataType: 'json'
                }
            });

            if (modal_type == "edit")
                edit_modal_on_open(modal_data);
        },
    });
}

async function modal_create_is_confirm(ajax_data) {
    let resp = await fetch('/api/product/', {
        credentials: 'same-origin', // 'include', default: 'omit'
        method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
        body: JSON.stringify(ajax_data), // Coordinate the body type with 'Content-Type'
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
    });

    try {
        json_obj = await resp.json();
        return json_obj;
    } catch (e) {
        return 'unknown error'
    }
}

async function modal_edit_is_confirm(modal_data, ajax_data) {
    let resp = await fetch('/api/product/' + modal_data.id, {
        credentials: 'same-origin', // 'include', default: 'omit'
        method: 'PUT', // 'GET', 'PUT', 'DELETE', etc.
        body: JSON.stringify(ajax_data), // Coordinate the body type with 'Content-Type'
        headers: new Headers({
            'Content-Type': 'application/json'
        }),
    });

    try {
        json_obj = await resp.json();
        return json_obj;
    } catch (e) {
        return 'unknown error'
    }
}

function edit_modal_on_open(modal_data) {
    let option_select_unit = new Option(modal_data.unit.name, modal_data.unit.id, false, false);
    let option_select_dish = new Option(modal_data.dish.name, modal_data.dish.id, false, false);
    $('.select-unit').append(option_select_unit).trigger('change');
    $('.select-dish').append(option_select_dish).trigger('change');

    $('input[name="input_name"]').val(modal_data.name);
    $('input[name="weight"]').val(modal_data.weight);
    $('.select-unit').select2('val', [modal_data.unit.id]);
    $('.select-dish').select2('val', [modal_data.dish.id]);
}