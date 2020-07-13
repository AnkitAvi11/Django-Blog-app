let likebutton = document.getElementById('like')


likebutton.addEventListener('click', function() {
    let blogid = document.getElementsByClassName('blogid')[0].getAttribute('id')
    let csrfToken = document.querySelector("#body > input[type=hidden]").value
    let form = new FormData()
    form.append('blogid', blogid)
    fetch(`http://127.0.0.1:8000/blog/like/`, {
        method : 'POST',
        body : form,
        headers : {
            'X-CSRFToken' : csrfToken
        }
    })
    .then(res => res.json())
    .then(data => {
        let classname = data.status;
        if (classname == 'far') {
            document.querySelector('#like').classList.remove('fas')
            document.querySelector('#like').classList.add('far')
            let likes = parseInt(document.getElementById('likecount').textContent)
            likes--;
            document.getElementById('likecount').textContent = likes
        }else{
            document.querySelector('#like').classList.remove('far')
            document.querySelector('#like').classList.add('fas')
            let likes = parseInt(document.getElementById('likecount').textContent)
            likes++;
            document.getElementById('likecount').textContent = likes
        }
    })
    .catch(err => console.log(err))
}, false)