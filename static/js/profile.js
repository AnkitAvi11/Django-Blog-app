let button = document.getElementById('change-dp')
let file = document.getElementById('file_profile')

button.onclick = () => {
    file.click()
}

file.addEventListener('change', (e) => {
    let files = file.files

    if(files && files[0]) {
        let form = new FormData()
        form.append('profile_pic', files[0])      

        let csrftoken = document.querySelector('#profile_pic > input[type=hidden]:nth-child(3)').value;
        console.log(csrftoken)

        fetch('http://127.0.0.1:8000/account/changeProfilePic/', {
            method : 'POST', 
            body : form,
            headers : {
                'X-CSRFToken' : csrftoken
            }
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            if(data.message == 'Error occurred') {
                alert("Profile could not be changed due to some errors")
            }else{
                let reader = new FileReader();

                reader.onload = (e) => {
                    document.getElementById('profile_pic').style.background = `url("${e.target.result}")`
                    document.getElementById('profile_pic').style.backgroundPosition = "center"
                    document.getElementById('profile_pic').style.backgroundSize = "cover"
                }

                reader.readAsDataURL(files[0])
            }
        })
        .catch(err => console.log(err));

        //  uncomment the code below when upload is done
        

    }else{
        console.log("no files chosed")
    }
});