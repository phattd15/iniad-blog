function callback(json) {
    let element = document.getElementById('like' + json.id);
    element.textContent = json.like;
}

function like(article_id) {
    fetch('/api/articles/' + article_id + '/like')
    .then(res => res.json())
    .then(callback)
}