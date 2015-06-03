grp.jQuery(function () {
    grp.jQuery('.message_help_text li strong').mousedown(function(){
        e = this; 
        if(window.getSelection) { 
            s = window.getSelection(); 
            if(s.setBaseAndExtent) { 
                s.setBaseAndExtent(e,0,e,e.innerText.length-1); 
            }
            else { 
                r = document.createRange(); 
                r.selectNodeContents(e); 
                s.removeAllRanges(); 
                s.addRange(r);
            } 
        }
        else if(document.getSelection) { 
            s = document.getSelection(); 
            r = document.createRange(); 
            r.selectNodeContents(e); 
            s.removeAllRanges(); 
            s.addRange(r); 
        }
        else if(document.selection) { 
            r = document.body.createTextRange(); 
            r.moveToElementText(e); 
            r.select();
        }
    });
});