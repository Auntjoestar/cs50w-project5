document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#editProfileButton").addEventListener("click", ()=> load_edit_info());
    document.querySelector(".editPicture").addEventListener("click", () => load_edit_picture());
    document.querySelectorAll(".cancelButton").forEach(element => element
    .addEventListener("click", ()=> load_profile_info()));
    load_profile_info();
});

function load_profile_info() {
    const info = document.querySelector(".userInformationView")
    const editInfo = document.querySelector(".editProfileView")
    const editPicture = document.querySelector(".editPictureView")
    info.style.display = "block"
    editInfo.style.display = "none"
    editPicture.style.display = "none"
    get_profile().then(result => {
        const userInformationView = document.querySelector(".userInformationView");
        userInformationView.innerHTML = `
                <h2>${result.name} ${result.lastname}</h2>
                <h3>${result.pronouns}</h3>
                <p>${result.bio}</p>
                <p>${result.birthdate}</p>
        `;
    });
}

function load_edit_info() {
    const info = document.querySelector(".userInformationView")
    const editInfo = document.querySelector(".editProfileView")
    const editPicture = document.querySelector(".editPictureView")
    info.style.display = "none"
    editInfo.style.display = "block"
    editPicture.style.display = "none"
    const form = document.querySelector("#edit-profile-form")
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        const name = document.querySelector("#id_first_name").value;
        const lastname = document.querySelector("#id_last_name").value;
        const bio = document.querySelector("#id_bio").value;
        const pronouns = document.querySelector("#id_pronouns").value;
        const date = document.querySelector("#id_birthdate").value;
        edit_profile(name, lastname, bio, pronouns, date).then(result => {
            if (result.error) {
                alert(result.error);
            } else {
                history.go(0);
            }
        });
    });
}

function load_edit_picture() {
    const info = document.querySelector(".userInformationView")
    const editInfo = document.querySelector(".editProfileView")
    const editPicture = document.querySelector(".editPictureView")
    info.style.display = "none"
    editInfo.style.display = "none"
    editPicture.style.display = "block"
}

async function edit_profile(name, lastname, bio, pronouns, date) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        'profile/edit',
        {method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            body: JSON.stringify({
                name: name,
                lastname: lastname,
                bio: bio,
                pronouns: pronouns,
                birthdate: date
            }),
            mode: 'same-origin'} 
    );
    const response = await fetch(request);
    const result = await response.json();
    return result;
}

async function get_profile() {
    const response = await fetch('profile');
    const result = await response.json();
    return result;
}