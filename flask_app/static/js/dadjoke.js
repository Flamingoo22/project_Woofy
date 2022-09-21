// URL = 'https://dad-jokes.p.rapidapi.com/random/joke'
// async function getRandom(){
//     // const dadjokes = document.getElementById('')
//     let response = await fetch(URL)
//     console.log(response)
//     let dadjokes = await response.json()
//     console.log(dadjokes)
// }

const options = {
	method: 'GET',
	headers: {
		'X-RapidAPI-Key': '6090547bb7mshb2ad3aa7af8f6fcp15001ejsn4c50ec57e140',
		'X-RapidAPI-Host': 'dad-jokes.p.rapidapi.com'
	}
};

const randJoke = document.getElementById('randJoke')
const question = document.getElementById('question')
const answer = document.getElementById('answer')
const donationPage = document.getElementById('donationPage')

fetch('https://dad-jokes.p.rapidapi.com/random/joke/', options)
	.then(response => response.json())
    .then(info => {
        question.innerHTML = `
        Q: ${info.body[0].setup}
        
        `
        answer.innerHTML = `
        A: ${info.body[0].punchline}
        `
        // var info = JSON.parse(response)
        // console.log(info.body)
    })
	.catch(err => {
        question.innerHTML =`
        WE OUT OF JOKES FOR TODAY, <br> COME BACK TOMORROW FOR MORE DAD JOKES:(
        <br>
        
        `
        randJoke.innerHTML = `
        NO MORE`
        randJoke.style.width = '400px'
        donationPage.innerHTML = `
        You can make a Differnece Right Now!<br>
        your gift will unlock unlimited dad jokes as you like!<br>
        ------donation page unavailable-------
        `
        console.error(err)
    });


btn = document.getElementById('btn')
const inside =()=>{
    return btn.innerHTML = 'WOOF WOOF!'
};
const outside =() =>{
    return btn.innerHTML = 'Enter Woofy'
}


function refresh(){
    setTimeout(function(){location.reload()}, 100);
    return;
}
randJoke.addEventListener('click', refresh)