let gAjax = (function() {
    const DataType = {
        TEXT : 'text',
        JSON : 'json'
    };
    const Method = {
        GET  : 'GET',
        POST : 'POST'
    };

    let _gAjax =class{
        constructor(selector_wait){    
            this.Selector_WAIT = selector_wait;
        }
        set url (value){                
            this._url = window.location.href + value
        }

        set wait(value){
            let method = value ? 'visible' : 'hidden';
            $(this.Selector_WAIT).css('visibility',method);
        }

        _get_ajax(success, data = null){
            let self = this;
            let _success = function(data){
                if (this._dataType  == DataType.TEXT && data.search(Regex.LOGIN_PASSWORD)>= 0){
                    window.location.href  = window.location.host;
                }

                success(data);            
                self.wait = false;
            }
            return $.ajax({
                    url:      this._url,
                    success:  _success,
                    data:     data,
                    dataType: this._dataType,
                    method:   this._method,
                    error:    function(jqXHR, textStatus, errorThrown){
                                    self.wait = false
                                    window.location.href = window.location.hostname;
                                }
                });
        }        
    }

    return {_gAjax,DataType,Method}
})();

export default gAjax