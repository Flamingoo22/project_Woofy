const commentOpen = []




function addPost(event){
    event.preventDefault()
    const postForm = document.getElementById('new_post')
    const postBody = document.querySelector('#posts')

    let formData = new FormData(postForm)
    fetch('/dashboard/post/create',{
        method:'POST',
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            // console.log(data)
            postBody.innerHTML += `
            <div class="container-sm bg-light rounded">
                <p>${data.creator}<p>
                <p>${data.form.created_at}
                <p>${data.form.content}</p>
                <a href='/posts/delete/${data.post_id}' class='btn'>Delete</a>
            </div>
            `
        })
        .catch(err => console.log(err))
}

function like(event, postId){
    event.preventDefault()
    if (event.target.innerHTML === 'favorite_border'){
        fetch ('/dashboard/like/' + postId)
        event.target.innerHTML = 'favorite'
        setTimeout(function(){location.reload()}, 10);
        return;
    }
    if (event.target.innerHTML === 'favorite'){
        event.preventDefault()
        fetch ('/dashboard/rm_like/' + postId)
        event.target.innerHTML = 'favorite_border'
        setTimeout(function(){location.reload()}, 10);
        return;
    }
}

function comment(e, postId){
    e.preventDefault()
    // document.getElementById(`btn${postId}`).setAttribute('disabled','true');
    const postForm = document.getElementById(`post${postId}`)
    const commentbox = document.getElementById(`commentbox${postId}`)
    // console.log(postForm)
    // console.log(commentbox)
    const commentInput = document.getElementById(`comment${postId}`)
    if(!commentOpen.includes(postId)){
        commentbox.style.display = 'block'
        postForm.innerHTML += `
        <div id="comment${postId}">
            <form action="/comments" class="navbar px-4" method="POST">
                <input type="hidden" name="post_id" value="${postId}">
                <textarea name="content" id="" class="form-control" cols="30" rows="5" placeholder="Write your comment here!"></textarea>
                <input type="submit" style='font-size:1.2em' class="btn">
            </form>
        </div>
        `
        commentOpen.push(postId)
    }
    else{
        commentbox.style.display = 'none'
        postForm.removeChild(commentInput)
        commentOpen.pop();
    }

    
}

function removeComment(e, commentId){
    e.preventDefault()
    fetch ('/comments/delete/' + commentId)
    setTimeout(function(){location.reload()}, 10);
    return;
}

function removePost(e, postId){
    e.preventDefault()
    fetch ('/posts/delete/' + postId)
    setTimeout(function(){location.reload()}, 10);
    return;
}