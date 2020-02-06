import gAjax from './gAjax.js';
/*!
  *    Module with class DinamicTable ((https://toomanof.ru))
  *    Copyrigh
  */
(function() {
    const Actions =  {
        APPEND_ITEM         :0,
        UPDATE_ITEM         :1
    };
    const Regex = {
        SectionForm         : new RegExp('<section class=\"forms\">.*<\/section>','i'),
        LOGIN_PASSWORD      : new RegExp('login-password','i')
    };
    const Classes ={
        SHOW             : 'md-show'    
    };
    const Selectors ={
        URL_ITEM            : '#url_item_table',
        DATA_TABLE          : '#table_data',
        TD                  : 'TD',
        TD_OPEN             : 'td:nth-child(n)td:not(:last-child)td:not(:first-child)',
        TD_ACTION           : 'tr td:last-child .action-remove',
        MD_FORM             : '#md-form',
        MD_WINDOW           : '#modal-form',
        MD_CONTENT          : '#modal-form .md-content',
        BTN_APPEND          : '.append-item',
        BTN_CLOSE           : '#md-close',
        BTN_SAVE            : '#md-save',
        ACTION_REMOVE       : '.action-remove',
        ACTION_DISPOSAL     : '.action-disposal',
        DATAPICKER          : '.datepicker',
        SELECT              : 'select[name="{0}"] option:selected',
        WAIT                : '.cssload-thecube'

    };   
    const Events ={
        CLICK_DATA          : `click`,
        INIT_DT             : `init.dt`
    };
    const Urls = {
        JSON                : 'json',
        RUSS_LANG           : '/static/DataTables/i18n/Russian.lang',
        APPEND_ITEM         : '/add',
        REMOVE_ITEM         : '/remove',
        DISPOSAL_ITEM       : '/disposal',

    };
    let  data_table;

    String.prototype.format = String.prototype.f = function(){
        var args = arguments;
        return this.replace(/\{(\d+)\}/g, function(m,n){
            return args[n] ? args[n] : m;
        });
    };
    class DinamicTable extends gAjax._gAjax{

        constructor(element) {
            super(Selectors.WAIT);
            let self = this;
            self._current_action = Actions.APPEND_ITEM;
            self._dataType  = gAjax.DataType.JSON;
            self._method    = gAjax.Method.GET;
            self.url = Urls.JSON;
            this.wait = true;
            self._get_ajax(function(data){
                self._data_table = $(element)
                                    .on(Classes.INIT_DT, function () {
                                        console.log( 'Table initialisation complete: '+new Date().getTime() );
                                    } )
                                    .DataTable({
                                        scrollY: 500,
                                        language: {url: Urls.RUSS_LANG},
                                        columns: data.columns,
                                        data:data.data,
                                    })
            });
        }

        set data(value){
            let current_page = this.page_info.page;
            
            if(this._current_action == Actions.UPDATE_ITEM){
                this.row.data(value);
                this.table.page(current_page).draw('page');
            }else if(this._current_action == Actions.APPEND_ITEM){
                this._data_table.row.add(value).draw().node();
            }
        }

        set target(value){   
            this._target = value;
            this.url = this.id;
        }
        
        get data(){   
            if($(this._target).prop("tagName") != Selectors.TD){
                this._target = $(this._target).parents(Selectors.TD);
            }
            return (this._target) ? this.row.data() : null;
        }

        get row(){
            return this._data_table.row(this._target);
        }

        get table(){        
            return this._data_table;
        }

        get page_info(){
            return this._data_table.page.info();
        }
        
        get id(){
            return this.data.id;
        }


        showForm(data_form){
            $(Selectors.MD_CONTENT).html(data_form.replace(/\n+/g, '').match(Regex.SectionForm));
            $(Selectors.MD_WINDOW).addClass(Classes.SHOW);
            $(Selectors.DATAPICKER).datepicker({format: 'dd.mm.yyyy'});
        }

        closeForm(){
            $(Selectors.MD_WINDOW).removeClass(Classes.SHOW);
            setTimeout(function(){$(Selectors.MD_CONTENT).html("")},200);            
        }

        openForm(){
            let self = this;
            this._dataType  = gAjax.DataType.TEXT;
            this._method    = gAjax.Method.GET;
            this.wait = true;
            this._get_ajax(
                function(data_form){
                    self.showForm(data_form);

                    //initialisation action close button
                    $(Selectors.BTN_CLOSE).on(Events.CLICK_DATA, (event) =>{
                        self.closeForm(event);
                    })    

                    //initialisation action close button
                    $(Selectors.BTN_SAVE).on(Events.CLICK_DATA,(event)=>{
                        self._onSaveForm(event);
                    })
                },
            );
        }

        readForm(data_form){
            let row_data = this.data;

            if(row_data == undefined){
                row_data = {'actions':'<button type="button" class="btn btn-info action-remove"\
                                       data-toggle="modal" data-target="#ModalQuestion">\
                                       <i class="fa fa-trash-o" aria-hidden="true"></i>\
                                       </button>',
                            'checks':'<div class="i-checks">\
                                        <input id="cb-15" type="checkbox" value="" class="form-control-custom">\
                                        <label style="float: left;" for="cb-15"></label>\
                                        </div>',
                            'id':this._max_id
                        };
            }
            $.each (data_form, function(index, val){
                row_data[val.name] = val.value;

                if ( $(Selectors.SELECT.format(val.name)).length > 0 ){
                    console.log(Selectors.SELECT.format(val.name),$(Selectors.SELECT.format(val.name)).text());
                    row_data[val.name] = $(Selectors.SELECT.format(val.name)).text();
                }
            })
            this.data = row_data;
        }       

        _onAppendItem(event){
            this.url =Urls.APPEND_ITEM;
            this._current_action = Actions.APPEND_ITEM;
            this.openForm();
        }

        _onUpdateItem(event){                
            this.target  = event.target;
            this._current_action = Actions.UPDATE_ITEM;
            this.openForm();
        }

        _onSaveForm(event){        
            let self = this;
            this._dataType  = gAjax.DataType.TEXT;
            this._method    = gAjax.Method.POST;
            let data_form   = $(Selectors.MD_FORM).serializeArray();
            this.wait = true;
            this._get_ajax(
                function(data){
                    if( self._current_action == Actions.APPEND_ITEM){
                        self.url = 'latest';
                        self._method = gAjax.Method.GET;
                        self._dataType = gAjax.DataType.JSON;
                        self._get_ajax(
                                function(data){
                                    self._max_id = data.id;
                                    self.readForm(data_form);
                                }
                        )
                    }
                },data_form
                
            )
            if(this._current_action == Actions.UPDATE_ITEM){
                this.readForm(data_form);
            }
            this.closeForm();
        }

        _onRemoveItem(event){
            this.target  = event.target;
            document.getElementById('form-remove-question').action = window.location.href + this.data.id + Urls.REMOVE_ITEM;
        }
    }  
    
    $(document)

    /**
    *------------------------------------------------------
    *
    *    Actions with data rows
    *
    *------------------------------------------------------
    */
        .on(Events.CLICK_DATA, Selectors.BTN_APPEND, function(event){
            data_table._onAppendItem(event);
        })
        .on(Events.CLICK_DATA, Selectors.ACTION_REMOVE, function(event){
            data_table._onRemoveItem(event);
        })

        .on(Events.CLICK_DATA, Selectors.ACTION_DISPOSAL, function(){
            $('#id_date_disposal').val((new Date()).format("d.m.Y"));
            document.getElementById('form-disposal-question').action = window.location.href + this.dataset.idElement+Urls.DISPOSAL_ITEM;
        })  
    /**
    *------------------------------------------------------
    *
    *    Actions data table
    *
    *------------------------------------------------------
    */
        .on(Events.CLICK_DATA, Selectors.TD_OPEN, (event) =>{
                data_table._onUpdateItem(event);
        })
    /**
    *------------------------------------------------------
    *
    *       Initialisation data table on ready document
    *
    *------------------------------------------------------
    */
        .ready( function(){
            if($('*').is(Selectors.DATA_TABLE))
                data_table = new DinamicTable(Selectors.DATA_TABLE);
        })
})();