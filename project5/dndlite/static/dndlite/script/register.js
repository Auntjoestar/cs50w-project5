document.addEventListener('DOMContentLoaded', function() {
    load_userForm();
});

function load_userForm() {
    document.querySelector(".userFormView").style.display = "block";
    document.querySelector(".profileFormView").style.display = "none";  
    document.querySelector(".imageFormView").style.display = "none"; 
    document.querySelector(".submitButton").style.display = "none";

    const navigationView = document.querySelector(".navigationView");
    navigationView.style.flexDirection = "column";
    
    const backButton = document.querySelector(".previousButton");
    backButton.style.display = "none";

    const nextButton = document.querySelector(".nextButton");
    nextButton.style.display = "block";
    nextButton.alignSelf = "flex-end";

    inputList = document.querySelectorAll(".userFormView input");
    console.log(inputList);
    nextButton.addEventListener("click", function(e) {
        e.preventDefault();
        valid = true;
        inputList.forEach(element => {
            if (!valid) {
                return;
            }
            valid = element.reportValidity();
        });
        if (valid) {
            load_profileForm();
        }
        });
    }

    


function load_profileForm() {
    document.querySelector(".userFormView").style.display = "none";
    document.querySelector(".profileFormView").style.display = "block";  
    document.querySelector(".imageFormView").style.display = "none";  

    const navigationView = document.querySelector(".navigationView");
    navigationView.style.flexDirection = "row";
    navigationView.style.justifyContent = "space-between";

    const backButton = document.querySelector(".previousButton");
    backButton.style.display = "block";
    backButton.alignSelf = "auto";
    backButton.addEventListener("click", function() {
        load_userForm();
    });

    const nextButton = document.querySelector(".nextButton");
    nextButton.style.display = "block";
    nextButton.alignSelf = "auto";
    const formInputs = document.querySelectorAll(".profileFormView input");
    console.log(formInputs);
    nextButton.addEventListener("click", function(e) {
        e.preventDefault();
        valid = true;
        formInputs.forEach(element => {
            if (!valid) {
                return;
            }
            valid = element.reportValidity();
        });
        if (valid) {
            load_imageForm();
        }
    });
}

function load_imageForm() {
    document.querySelector(".userFormView").style.display = "none";
    document.querySelector(".profileFormView").style.display = "none";  
    document.querySelector(".imageFormView").style.display = "block"; 
    document.querySelector(".submitButton").style.display = "block"; 

    const navigationView = document.querySelector(".navigationView");
    navigationView.style.flexDirection = "column";

    const backButton = document.querySelector(".previousButton");
    backButton.style.display = "block";
    backButton.alignSelf = "flex-start";

    backButton.addEventListener("click", function() {
        load_profileForm();
    });

    const nextButton = document.querySelector(".nextButton");
    nextButton.style.display = "none";
}