document.addEventListener('DOMContentLoaded', function() {
    
    const editBtns = document.querySelectorAll('.edit-item__btn');

    editBtns.forEach(element => {

        element.addEventListener('click', function() {
            tr_el = this.parentElement.parentElement;
            tr_Children = tr_el.children;

            document.querySelector("#InputItemId__edit").value = tr_Children[1].innerText;
            document.querySelector("#InputItemName__edit").value = tr_Children[2].innerText;
            document.querySelector("#InputItemDescription__edit").value = tr_Children[3].innerText;
            document.querySelector("#InputItemCategory__edit").value = tr_Children[4].innerText;
            document.querySelector("#InputItemPrice__edit").value = tr_Children[5].innerText.substring(1);
            document.querySelector("#InputItemPhotoUrl__edit").value = tr_Children[7].innerText;

            // Checkbox handling
            availablity = document.querySelector("#InputItemAvailability__edit")
            availablity.value = tr_Children[6].innerText;

            
            check_availability(availablity.value);


            availablity.addEventListener('change', function() {
                if (this.checked) {
                    availablity.value = "True"
                } else {
                    availablity.value = "False"
                }
            });

            // Submit edit button handling
            let submitEditBtn = document.querySelector("#submit-edit__btn"), elClone = submitEditBtn.cloneNode(true);
            submitEditBtn.parentNode.replaceChild(elClone, submitEditBtn);

            elClone.addEventListener('click', update_item)

            // Close edit button handling
            document.querySelector("#close-edit__btn").addEventListener('click', function() {
                document.querySelector("#edit-item__modal").style.display = "none";
                document.querySelector(".backdrop").style.display = "none";
            })

            // Showing edit model
            const modalEl = document.querySelector("#edit-item__modal");
            modalEl.style.display = "block";
            document.querySelector(".backdrop").style.display = "block";
            
        })

    });


    // TO DO

})


// Custom Functions
function check_availability(availablity_state) {
    console.log(availablity_state);
    if (availablity_state === "True") {
        availablity.checked = true;
    } else {
        availablity.checked = false;
    }
}



// API requests
function update_item() {

    // Make JSON with the new values for the Item

    const item_vals = {
        "id": document.querySelector("#InputItemId__edit").value,
        "name": document.querySelector("#InputItemName__edit").value,
        "description": document.querySelector("#InputItemDescription__edit").value,
        "category": document.querySelector("#InputItemCategory__edit").value,
        "price": document.querySelector("#InputItemPrice__edit").value,
        "photoUrl": document.querySelector("#InputItemPhotoUrl__edit").value,
        "availability": document.querySelector("#InputItemAvailability__edit").value
    }

    fetch('/itemedit', {
        method: 'PUT',
        body: JSON.stringify(item_vals)
    }).then(
        () => {
            tr_Children[1].innerText = item_vals.id
            tr_Children[2].innerText = item_vals.name
            tr_Children[3].innerText = item_vals.description
            tr_Children[4].innerText = item_vals.category
            tr_Children[5].innerText = "$" + item_vals.price
            tr_Children[7].innerText = item_vals.photoUrl
            tr_Children[6].innerText = item_vals.availability;
        }
    )

    // Close the Modal after update
    document.querySelector("#edit-item__modal").style.display = "none";
    document.querySelector(".backdrop").style.display = "none";
}
