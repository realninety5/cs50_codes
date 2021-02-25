
let follow = document.getElementById('follow')
if (follow){
    follow.addEventListener('click', (e) => {
        let head = document.getElementById('head');
        let head_content = head.textContent;
            e.preventDefault();
            let todo = (follow.textContent == 'Follow') ? 'Unfollow' : 'Follow';
            fetch('follow/', {
                method: 'PUT',
                body: JSON.stringify({
                    username: document.getElementById('who').textContent,
                    follow: follow.textContent
                })
            })
        let count = document.getElementById('count');
        if (follow.textContent == 'Follow'){
            count.textContent = parseInt(count.textContent) + 1;
        } else {
            count.textContent = parseInt(count.textContent) - 1;
        }
        follow.textContent = todo;
    })
}



document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement
    if (target.className == 'like') {
        let todo = (target.style.color == 'gray') ? 'Like' : 'Unlike';
        fetch(`like/${target.id}/`, {
            method: 'PUT',
            body: JSON.stringify({
                post: target.id,
                like: todo
            })
        })
        let count_like = document.getElementById(`count_like${target.id}`);
        if (target.style.color == 'gray'){
            target.style.color = 'red';
            count_like.textContent = parseInt(count_like.textContent) + 1;
        } else {
            target.style.color = 'gray';
            count_like.textContent = parseInt(count_like.textContent) - 1;
        }
    }
}, false);

document.addEventListener('click', (e) => {
    e = e || window.event;
    var target = e.target || e.srcElement;
    if (target.className == 'editit') {
        let id = target.id.split('-')[1];
        let update_post = document.getElementById(`update-post${id}`);
        update_post.style.display = 'block';
        let new_text = document.getElementById(`textArea${id}`);
        let old_post = document.getElementById(`oldPost${id}`);
        new_text.value = old_post.textContent;
        new_text.focus();
        document.getElementById(`update${id}`).addEventListener('click', e => {
            fetch('edit/', {
                method: 'PUT',
                body: JSON.stringify({
                    new_body: new_text.value,
                    old_body: id
                })
            })
        old_post.textContent = new_text.value;
        update_post.style.display = 'none';
        })
    }
}, false);


