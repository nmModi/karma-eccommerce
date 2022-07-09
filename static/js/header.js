var el = document.getElementsByClassName('nav-item')
    var active_url = document.location.href;
    for (var i=0; i<el.length; i++) {
        var a = el[i].querySelector('a');
        if (active_url==a.href){
            console.log(active_url + ' ' + a.href)
            el[i].classList.add('active');
            break;
        }
    }
