document.addEventListener('DOMContentLoaded', function() {
    
    const editBtns = document.querySelectorAll('.edit-item__btn');

    editBtns.forEach(element => {

        element.addEventListener('click', function() {
            tr_el = this.parentElement.parentElement;
            tr_Children = tr_el.children;

            document.querySelector("#InputItemName__edit").value = tr_Children[1].innerText;
            document.querySelector("#InputItemDescription__edit").value = tr_Children[2].innerText;
            document.querySelector("#InputItemCategory__edit").value = tr_Children[3].innerText;
            document.querySelector("#InputItemPrice__edit").value = tr_Children[4].innerText.substring(1);
            document.querySelector("#InputItemPhotoUrl__edit").value = tr_Children[6].innerText;

            // Checkbox handling
            availablity = document.querySelector("#InputItemAvailability__edit")
            availablity.value = tr_Children[5].innerText;

            if (availablity.value === "True") {
                availablity.checked = true;
            } else {
                availablity.checked = false;
            }

            // Submit edit button handling
            let submitEditBtn = document.querySelector("#submit-edit__btn"), elClone = submitEditBtn.cloneNode(true);
            submitEditBtn.parentNode.replaceChild(elClone, submitEditBtn);
                

            elClone.addEventListener('click', function() {
                console.log(availablity)
            })

            // Close edit button handling
            document.querySelector("#close-edit__btn").addEventListener('click', function() {
                document.querySelector("#edit-item__modal").style.display = "none";
                document.querySelector(".backdrop").style.display = "none";
            })

            // Showing edit model
            const modalEl = document.querySelector("#edit-item__modal");
            console.log(modalEl)
            modalEl.style.display = "block";
            document.querySelector(".backdrop").style.display = "block";
            
        })

    });


    // TO DO

})


