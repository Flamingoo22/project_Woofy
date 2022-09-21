
const editBtn = document.getElementById('edit_btn')
const formClose = document.getElementById('hide_form')


const showForm = function(){
    event.preventDefault();
    const profileForm = document.getElementById('profileForm')
    fetch('/woofy/user_update',{
        method:'GET',
    })
        .then(res => res.json())
        .then(data => {
            console.log(data.dob)
            profileForm.innerHTML = `
            <form onsubmit="updateUser(event)" id="edit_profile" style='margin-top:-40px'>
                <div class="navbar">
                    <label for="username" class="form-label" style="font-size:1.6rem">Username:</label>
                    <button type="button" id="hide_form" style='background:none'>
                        <span class="material-icons" >close</span>
                    </button>
                </div>
                <input type="text" name="username" class="form-control" style='margin-top:-40px' value="${data.username}" style="font-size:1.6rem">
                <label for="dob" class="form-label" style="font-size:1.6rem">Date of Birth:</label>
                <input type="date" name="dob" class="form-control" id="" value="${data.dob}" style='margin-top:-30px'>
                <input type="submit" name="" id="" class="btn" style="font-size:1.6rem">
            </form>
            `
        })
        .then(closeRes => 
            profileForm.querySelector('#hide_form').addEventListener('click', ()=>{
            setTimeout(function(){location.reload()}, 10)
        }))
        .catch(err => console.log(err));
}
editBtn.addEventListener('click', showForm);

function updateUser(event){
    event.preventDefault()

    const updateForm = document.getElementById('edit_profile')
    let formData = new FormData(updateForm)
    fetch('/woofy/update',{
        method:'POST',
        body:formData
    })
    profileForm.style.display = 'none';
    setTimeout(function(){location.reload()}, 10);
}

function updatePost(event, postId){
    event.preventDefault();
    const post = document.getElementById(`post${postId}`);
    const updateForm = document.querySelector(`#postUpdateForm${postId}`)
    console.log(updateForm)
    fetch('/woofy/user_page/'+postId,{
        method:'GET',
    })
        .then(res => res.json())
        .then(data => {
            post.innerHTML = `
            <div id='postUpdateForm${postId}'>
                <form action="/woofy/user_page/update" class="container bg-light rounded p-1 d-flex flex-column" method='POST'>
                    <input type="hidden" name="id" value="${postId}">
                    <div class='navbar'>
                    <label for="">Title:</label>
                    <button type="button" id='closeEdit'>
                    <span class="material-icons">close</span>
                    </button>
                    </div>
                    <input type="text" name="title" class='form-control' value='${data.title}'>
                    <label for="">Content:</label>
                    <textarea name="content" cols="30" rows="5">${data.content}</textarea>
                    <input type="submit" value="Update">
                </form>
            </div>
            `
        })
        .then(closeRes => 
            post.querySelector('#closeEdit').addEventListener('click', ()=>{
            setTimeout(function(){location.reload()}, 100)
        }))
        .catch(err => console.log(err));
    }