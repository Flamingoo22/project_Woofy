function showModal() {
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.innerHTML = `
    <div class="modal_inner" style="background-color: rgba(251, 193, 1, 0.801);">
        <form onsubmit="addPost(event)" id="new_post" class="container bg-light rounded p-3 d-flex flex-column gap-3">
            <div class="modal_top">
                <div class="modal_title text-center" style="font-size:2em">Make a Post!</div>
                <button class="modal_close" type="button">
                    <span class="material-icons">close</span>
                </button>
            </div>
            <div class="modal_content">
                <div class="d-flex">
                    <label for="title"  style='font-size:2rem'>Title:</label>
                    <input type="text" name="title" id="title" class="form-control" style='font-size:1.6rem'>
                </div>
                <textarea name="content" id="content" class="form-control" style="border:none; font-size:1.6rem" placeholder="What's in your mind?"></textarea>
            </div>
            <div class="modal_bottm">
                <input type="submit" class="btn mt-4" id='post_submit' style="width:100% ; background-color: rgb(207, 210, 213); font-size:1.2em">
            </div>
        </form>
    </div>
    `;
    
    modal.querySelector('.modal_close').addEventListener('click', ()=>{
        document.body.removeChild(modal);
    })
    modal.querySelector('#post_submit').addEventListener('click', ()=>{
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
                console.log(data)
                setTimeout(function(){location.reload()}, 1000);
            })
            .catch(err => console.log(err))
        document.body.removeChild(modal);
    })
    document.body.appendChild(modal)
}

function addPost(e){
    e.preventDefault();
    e.addEventListener('click', showModal())
}