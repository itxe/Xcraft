window.onpopstate = function (event) {
    document.getElementById('petch_content').innerHTML = '';
    setTimeout("petch_display()", 100)
    petch_request(null, event.currentTarget.location.pathname)
}

function petch(title, page_path) {
    document.getElementById('petch_content').innerHTML = '';
    setTimeout("petch_display()", 100)
    petch_request(title, page_path)
    window.history.pushState({}, title, page_path)
}

function petch_display() {
    if (document.getElementById('petch_content').innerHTML == '') {
        document.getElementById('petch_content').innerHTML = '<h1 style="text-align:center;font-size:64px;color:gray;margin-top:30%;">请求中...</h1>';
    }
}

function petch_request(title, page_path) {
    fetch(page_path + '?petch=true')
        .then(res => res.text())
        .then(function (res) {
            document.getElementById('petch_content').innerHTML = res;
            if(title != null){
                document.title = title
            }
            window.eval('<script src="/static/js/mdui.min.js"></script>')
        })
}