import gAjax from '/static/root/js/gAjax.js';
/*!
  *    Module with class Logging ((https://toomanof.ru))
  *    Copyrigh
  */
(function() {    
    const  ITEM_LOGGING='<li class="d-flex justify-content-between">\
                          <div class="left-col d-flex">\
                            <div class="icon"><i class="icon-rss-feed"></i></div>\
                            <div class="title"><strong>!dchp_message!</strong>\
                              <p class="logging">!logging!</p>\
                            </div>\
                          </div>\
                          <div class="right-col text-right">\
                            <div class="update-date">!month!<span class="month">!date!</span></div>\
                          </div>\
                        </li>'

    const Regex_ = {        
        SECTIONFORM    : new RegExp('<section class=\"forms\">.*<\/section>','i'),
        LOGIN_PASSWORD : new RegExp('login-password','i'),
        MONTH : /^[A-Z]{1}[a-z]{2}\s*\d{1,2}/i,
        DATE : /\d{1,2}:\d{1,2}:\d{1,2}/i,
        LOG_TEXT: /DHCP[A-Z]+ (.*)/i,
        DHCPMESSAGE :/DHCP[A-Z]+/g
    }

    const Urls = {
        JSON : 'json'
    }
    const array_for_find =[
        {'reg':Regex_.MONTH,
         'reg_replace':/!month!/g
        },
        {'reg':Regex_.DATE,
         'reg_replace':/!date!/g
        },
        {'reg':Regex_.LOG_TEXT,
         'reg_replace':/!logging!/g
        },
        {'reg':Regex_.DHCPMESSAGE,
         'reg_replace':/!dchp_message!/g
        },
    ]
     class Logging extends gAjax._gAjax{

        constructor(element, only='*') {
            super();            
            this.element = $(element);
            this.only = only;
            self = this;         
            self.get_log_record();
            setInterval(function(){self.get_log_record()},10000);
        }

        add_item(item_data){
            let self = this;
            let item_html = ITEM_LOGGING;
            $.each(array_for_find,function(index, item){
                item_html = self._replace(item_data, item_html,item)
            });
            return item_html;
        }

        get_log_record(){
            let log_html = '';
            let self = this;
            self.url = Urls.JSON;
            self._dataType = gAjax.DataType.JSON;
            self._method = gAjax.Method.GET;
            
            self. _get_ajax(function(data){
                let tmp_html;
                let items = data.data.split(/\n/).reverse();
                items.shift();
               $.each(items, function(index, val){
                    tmp_html = self.add_item(val);
                    if( tmp_html !== false){
                        log_html += tmp_html;
                    }
                });

                self.element.html(log_html);         
            });
        }
        _replace(item_data,item_html,item){
            let s;
            let tmp_html = item_html; ;

            if((s = item.reg.exec(item_data)) !==null) {
                item_html = item_html.replace(item.reg_replace,s[1] !==undefined ? s[1]: s[0]);
            }         
            return tmp_html !== item_html ? item_html:false;
        }
    }
    $(document)
    .ready( function(){
       let logging = new Logging('#logging');
    });
})();