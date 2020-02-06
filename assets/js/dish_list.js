$(document).ready(function () {
    dtable = $('#dish_list').DataTable({
        ajax: {
            url: '/api/dish_get/?format=datatables',
        },

        "columns": [
            {"title": "Наименование", "data": "name"},
            {"title": "Ед. изм.", "data": "unit.name"},
            {"title": "Выход порции", "data": "out"},
            {"title": "Технологическая карта", "data": "tech_map.name"},
        ],
        "language": ru_local,
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
        width: 480,
        html: '<div class = "form-group">' +
            '<div class="form-row"><label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Название:</label></div>' +
            '<div class="form-row"><input name="input-name" type="text" class="form-control form-control-sm" style="border-color:#AAAAAA;"></div>' +
            '<div class="form-row"><div name="name-error-msg" style="display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div></div>' +
            '<div class="form-row"><label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Ед. изм:</label></div>' +
            '<div class="form-row" style="margin-bottom:5px;"><select class="select-unit js-example-basic-single"></select></div>' +
            '<div class="form-row"><label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Выход порции:</label></div>' +
            '<div class="form-row"><input name="out-weight" class="form-control form-control-sm" type="number" step="any" style="border-color:#AAAAAA;"/></div>' +
            '<div class="form-row"><div name="weight-error-msg" style="display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div></div>' +
            '<div class="form-row"><label style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Технологическая карта:</label></div>' +
            '<div class="form-row" style="margin-bottom:5px;"><select class="select-tech-map js-example-basic-single"></select></div>' +
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
                tech_map: $('.select-tech-map').val(),
                name: $('input[name="input-name"]').val(),
                out: $('input[name="out-weight"]').val()
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

                console.log(res.data)
                if (modal_type == "create")
                    dtable.row.add(res.data).draw();
            } else if (res.status == "failed" && res.data.indexOf("UNIQUE") != -1) {
                $('div[name="name-error-msg"]').text('Это поле должно быть уникальным')
            } else {
                if (res.hasOwnProperty('name')) {
                    $('div[name="name-error-msg"]').text('Это поле не может быть пустым')
                }
                if (res.hasOwnProperty('out')) {
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
            $('.select-tech-map').select2({
                width: '100%',
                ajax: {
                    url: '/api/select2/map/',
                    dataType: 'json'
                }
            });

            if (modal_type == "edit")
                edit_modal_on_open(modal_data);
        },
    });
}

async function modal_create_is_confirm(ajax_data) {
    let resp = await fetch('/api/dish/', {
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
    let resp = await fetch('/api/dish/' + modal_data.id, {
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
    let option_select_tech_map = new Option(modal_data.tech_map.name, modal_data.tech_map.id, false, false);
    $('.select-unit').append(option_select_unit).trigger('change');
    $('.select-tech-map').append(option_select_tech_map).trigger('change');

    $('input[name="input-name"]').val(modal_data.name);
    $('input[name="out-weight"]').val(modal_data.out);
    $('.select-unit').select2('val', [modal_data.unit.id]);
    $('.select-tech-map').select2('val', [modal_data.tech_map.id]);
}