$(document).ready(function () {
    $('#example').DataTable({
        "language": ru_local,
        ajax: {
            url: '/api/map_get/?format=datatables',
        },
        "columns": [
            {"title": "Наименование", "data": "name"},
            {"title": "Источник", "data": "source"},
            {"title": "Выход порции", "data": "batch_output"},
            {"title": "Ед. изм", "data": "unit"},
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
        width: 960,
        html:
            '<div class="form-row loading-info" style="display:inline-block;font-size:24px;color:rgb(255,172,33);margin-bottom:5px;margin-left:5px;""></div>' +
            '<div class="form-group form-content">' +
            '<div class="form-row"  style="margin-bottom: 15px;">' +
            '   <div class="col-5">' +
            '       <label class="form-row" style="color:rgb(0,0,0);">Утверждено:</label>' +
            '       <div class="form-row"><select class="select-map-approved js-example-basic-single" ></select></div>' +
            '   </div>' +
            '   <div class="col-2"></div>' +
            '   <div class="col-5">' +
            '       <label class="form-row" style="color:rgb(0,0,0);">Согласовано:</label>' +
            '       <div class="form-row"><select class="select-map-agreed js-example-basic-single"></select></div>' +
            '   </div>' +
            '</div>' +
            '<div class="form-row"  style="margin-bottom: 15px;">' +
            '   <div class="col-5">' +
            '       <label class="form-row" style="color:rgb(0,0,0);">Название:</label>' +
            '       <input name="input-name" type="text" class="form-row form-control form-control-sm" style="border-color:#AAAAAA;">' +
            '       <div name="name-error-msg" style="float:left;display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div>' +
            '   </div>' +
            '   <div class="col-2"></div>' +
            '   <div class="col-5">' +
            '       <label class="form-row" style="color:rgb(0,0,0);">Источник:</label>' +
            '       <input name="input-source" type="text" class="form-row form-control form-control-sm" style="border-color:#AAAAAA; margin-right: -5px;">' +
            '   </div>' +
            '</div>' +
            '<div class="form-row"><label style="color:rgb(0,0,0);">Технология приготовления:</label></div>' +
            '<div class="form-row" style="margin-bottom: 15px;">' +
            '   <textarea name="technology" rows="5" class="form-control" required="" id="id_technology"></textarea>' +
            '   <div name="technology-error-msg" style="display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div>' +
            '</div>' +
            '<div class="form-row" style="text-align:left;">' +
            '<table id="table_ingredients" class="table table-striped table-sm" style="width:100%">' +
            '   <thead>' +
            '       <tr>' +
            '           <th style="width: 5%;">№</th>' +
            '           <th style="width: 30%;">Ингридиенты</th>' +
            '           <th style="width: 30%;">Брутто</th>' +
            '           <th style="width: 30%;">Нетто</th>' +
            '           <th style="width: 5%;"></th>' +
            '       </tr>' +
            '   </thead>' +
            '   <tbody></tbody>' +
            '   <tfoot><th></th><td style="text-align:center;"><div name="product-error-msg" style=" display:inline-block;font-size:12px;color:rgb(255,0,0);margin-bottom:5px;margin-left:5px;"></div></td><th></th><th></th><th></th></tfoot>' +
            '</table>' +
            '</div>' +
            '<div class="form-row" style="margin-bottom: 15px;"><button type="button" class="btn btn-primary" onclick="append_row(null)">Добавить</button></div>' +
            '<div class="form-row">' +
            '   <div class="col-5">' +
            '       <label class="form-row" style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Ед. изм:</label>' +
            '       <div class="form-row">' +
            '           <select class="select-unit js-example-basic-single"></select>' +
            '       </div>' +
            '   </div>' +
            '<div class="col-2"></div>' +
            '   <div class="col-5">' +
            '       <label class="form-row" style="color:rgb(0,0,0); margin: 0px 0px 5px 3px;">Выход порции:</label>' +
            '       <input name="out-weight" class="form-row form-control form-control-sm" type="number" step="any" style="border-color:#AAAAAA; height: 28px;"/>' +
            '   </div>' +
            '</div>' +
            '</div>',
        confirmButtonText: 'Подтвердить',
        cancelButtonText: 'Отменить',
        buttonsStyling: true,
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        background: "rgb(255,255,255)",
        preConfirm: async function () {
            let ajax_data = {
                map: {
                    name: $('input[name="input-name"]').val(),
                    source: $('input[name="input-source"]').val(),
                    approved: $('.select-map-approved').val(),
                    agreed: $('.select-map-agreed').val(),
                    technology: $('textarea[name="technology"]').val(),
                    batch_output: $('input[name="out-weight"]').val(),
                    unit: $('.select-unit').val(),
                },
                items: []
            };

            let elements_position = document.getElementsByName("position");
            let elements_brutto = document.getElementsByName('item-brutto');
            let elements_netto = document.getElementsByName('item-netto');
            let elements_select_product = document.getElementsByName('select-product');
            let elements_item_id = document.getElementsByName('item-id');

            for (let i = 0; i < elements_position.length; i++) {
                ajax_data.items.push({
                    id: elements_item_id[i].value,
                    position: elements_position[i].innerText,
                    product: elements_select_product[i].value,
                    brutto: elements_brutto[i].value,
                    netto: elements_netto[i].value,
                });
            }

            console.log(ajax_data);
            $('div[name="name-error-msg"]').text('');
            $('div[name="technology-error-msg"]').text('');
            $('div[name="product-error-msg"]').text('');

            if (modal_type == "create")
                res = await modal_create_is_confirm(ajax_data);
            else if (modal_type == "edit")
                res = await modal_edit_is_confirm(modal_data, ajax_data);

            if (res.hasOwnProperty('name')) {
                $('div[name="name-error-msg"]').text('Это поле не может быть пустым')
            }
            if (res.hasOwnProperty('technology')) {
                $('div[name="technology-error-msg"]').text('Это поле не может быть пустым')
            }
            if (res.hasOwnProperty('product')) {
                $('div[name="product-error-msg"]').text('Это поле не может быть пустым')
            }

            return false;
        },
        onOpen: async function () {
            $('.select-unit').select2({
                width: '100%',
                ajax: {
                    url: '/api/select2/unit/',
                    dataType: 'json'
                }
            });

            $('.select-map-approved').select2({
                width: '97%',
                ajax: {
                    url: '/api/people/',
                    dataType: 'json'
                }
            });

            $('.select-map-agreed').select2({
                width: '97%',
                ajax: {
                    url: '/api/people/',
                    dataType: 'json'
                }
            });

            if (modal_type == "edit") {
                $('.loading-info').text('Идет загрузка данных...');
                $('.form-content').css('display', 'none');
                res = await modal_edit_get_data(modal_data.id);
                $('.loading-info').text('Заполняется форма...');
                edit_modal_on_open(res);
                $('.loading-info').text('');
                $('.form-content').css('display', 'block');

            }

        },
    });
}


function delete_row(row) {
    $('tbody', 'table#table_ingredients')[0].removeChild(row);

    let elements_position = document.getElementsByName("position");
    for (let i = 0; i < elements_position.length; i++) {
        elements_position[i].innerText = i + 1;
    }
}


function append_row(row_data) {
    $('tbody', 'table#table_ingredients').append(
        '<tr>' +
        '   <td name="position" style="width: 5%;"><input name="item-id" type="hidden" value="' + (row_data ? row_data.id : -1) + '">' + ($('tbody', 'table#table_ingredients')[0].childNodes.length + 1) + '</td>' +
        '   <td style="width: 30%;"><select name="select-product" class="select-product js-example-basic-single"></select></td>' +
        '   <td style="width: 30%;"><input type="number" name="item-brutto" value="' + (row_data ? row_data.brutto : 0) + '" class="form-control form-control-sm mr-3" required="" data-msg="Укажите брутто" step="0.001"></td>' +
        '   <td style="width: 30%;"><input type="number" name="item-netto" value="' + (row_data ? row_data.netto : 0) + '" class="form-control form-control-sm mr-3" required="" data-msg="Укажите нетто" step="0.001"></td>' +
        '   <td style="width: 5%;"><button type="button" class="btn btn-danger" onclick="delete_row(this.parentElement.parentElement)">X</button></td>' +
        '</tr>');


    $('.select-product').select2({
        width: '100%',
        ajax: {
            url: '/api/select2/product/',
            dataType: 'json'
        }
    });

    if (row_data) {
        let option_product = new Option(row_data.product.text, row_data.product.id, false, false);
        $('.select-product').append(option_product).trigger('change');
    }
}


async function modal_create_is_confirm(ajax_data) {
    let resp = await fetch('/api/map/', {
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
    let resp = await fetch('/api/map/' + modal_data.id, {
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
    $('input[name="input-name"]').val(modal_data.name);
    $('input[name="input-source"]').val(modal_data.source);
    $('textarea[name="technology"]').val(modal_data.technology);
    $('input[name="out-weight"]').val(modal_data.batch_output);

    let option_unit = new Option(modal_data.unit.text, modal_data.unit.id, false, false);
    let option_map_agreed = new Option(modal_data.agreed.text, modal_data.agreed.id, false, false);
    let option_map_approved = new Option(modal_data.approved.text, modal_data.approved.id, false, false);
    $('.select-unit').append(option_unit).trigger('change');
    $('.select-map-agreed').append(option_map_agreed).trigger('change');
    $('.select-map-approved').append(option_map_approved).trigger('change');

    for (item of modal_data.items) {
        append_row(item);
    }
}


async function modal_edit_get_data(obj_id) {
    let resp = await fetch('/api/map_full/' + obj_id, {
        credentials: 'same-origin', // 'include', default: 'omit'
        method: 'GET', // 'GET', 'PUT', 'DELETE', etc.
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