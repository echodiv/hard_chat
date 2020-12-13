var load_button = document.getElementById('load_posts_btn');
var template = document.querySelector("#post_template");
var scroller = document.querySelector("#scroller");
var sentinel = document.querySelector("#sentinel");
var counter = 1;
var user_id = window.location.pathname.split('/').pop();
var load_posts = true;

console.log(user_id)
if (user_id == 'explore'){
    var load_uri = '/followed_posts';
} else {
    var load_uri = `/user_posts/${user_id}`;
}

function loadItems() {
    fetch(`${load_uri}?page=${counter}`).then((response) => {
    response.json().then((data) => {
    if (data['items'].length == 0) {
        sentinel.innerHTML = "No more posts"
        load_button.hidden = true;
        load_posts = false;
        return;
    }
    for (var i=0; i < data['items'].length; i++) {
        let template_clone = template.content.cloneNode(true);
        template_clone.querySelector('#content').innerHTML =  data['items'][i]['post_content'];
        var post_date = moment(data['items'][i]['post_time']).fromNow();
        var author = data['items'][i]['author'];
        template_clone.querySelector('#post_author').innerHTML =  `<a href="/user/${author['id']}">${author['name']} ${author['sename']}</a> ${post_date}`;
        scroller.appendChild(template_clone);
    }
    counter += 1;
})
})
}
var callbackFunction = function(entries){
    if (!load_posts){
        return;
    }
    loadItems();
}

var intersectionObserver = new IntersectionObserver(callbackFunction, {
    threshold: 0.1
});

if (sentinel){
    intersectionObserver.observe(sentinel);
}

if (load_button){
    load_button.onclick = loadItems;
}