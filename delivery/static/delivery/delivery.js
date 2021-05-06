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


    // CART SECTION
    let cartBtns = document.querySelectorAll(".add-cart__btn");
    cartBtns.forEach(element => {
        element.addEventListener('click', function() {

            let children = this.parentElement.parentElement.children

            // Get item name
            let itemName = children[0].innerText;

            // Get amount
            let targetDiv = children[4];
            let targetDivChildren = targetDiv.children;
            let amount = targetDivChildren[1].value;

            // Validate amount value
            if (amount === "" || amount < 1) {
                alert("Invalid amount!")
                targetDivChildren[1].value = '';
                throw new Error("Invalid amount!");
            }

            targetDivChildren[1].value = '';

            // Validate input product name
            let added_productNames = document.querySelectorAll(".product-name");
            if (added_productNames !== null) {
                added_productNames.forEach(element => {
                    if (element.innerText === itemName) {
                        alert("This Product is already added!")
                        targetDivChildren[1].value = '';
                        throw new Error("This Product is already added!");
                    }
                });
            }

            // Get Price
            const mainDiv = this.parentElement.parentElement.parentElement.children;
            const price = mainDiv[0].innerText;

            // Count total price for every record:
            let amounti = parseInt(amount);
            let pricef = parseFloat(price.substring(1));
            let totalPrice = amounti * pricef;

            newTr = document.createElement("tr");
            newTr.classList.add("cart-item__row");

            newTd_name = document.createElement("td");
            newTd_name.innerText = itemName;
            newTd_name.classList.add("product-name");

            newTd_amount = document.createElement("td");
            newTd_amount.innerText = amount;

            newTd_price = document.createElement("td");
            newTd_price.innerText = price;

            newTd_tprice = document.createElement("td");
            newTd_tprice.innerText = "$" + totalPrice;
            newTd_tprice.classList.add("total-price");

            newTr.append(newTd_name)
            newTr.append(newTd_amount)
            newTr.append(newTd_price)
            newTr.append(newTd_tprice)
            const tableData = document.querySelector("#customer-cart__table > tbody")
            returnedNode = tableData.insertBefore(newTr, tableData.lastElementChild)

            // Update The Total Cost
            totalCost = 0;
            document.querySelectorAll(".total-price").forEach(element => {
                totalCost += parseFloat(element.innerText.substring(1));
                document.querySelector("#total-cost__value").innerText = "$" + totalCost;
            });


        })
    });

    // Add Reset Functionality
    document.querySelector("#reset-cart__btn").addEventListener('click', function() {
        document.querySelector("#customer-cart__table > tbody").innerHTML = '';
        document.querySelector("#total-cost__value").innerText = '';
    })

    // Add Submitting Order Functionlity
    document.querySelector("#submit-cart__btn").addEventListener('click', function() {
        orderItems = []
        let cartItms = document.querySelectorAll(".cart-item__row");
        cartItms.forEach(element => {
            const ch = element.children;
            const obj = {
                "name": ch[0].innerText.toLowerCase(),
                "amount": parseInt(ch[1].innerText)
            }

            orderItems.push(obj);
        });

        // Make Order Request
        fetch("/mkorder", {
            method: 'POST',
            body: JSON.stringify(orderItems)
        }).then(
            response => {
                console.log(response);
                document.querySelector("#customer-cart__table > tbody").innerHTML = '';
                document.querySelector("#total-cost__value").innerText = '';
            }
        )
    })

})


// Custom Functions
function check_availability(availablity_state) {
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
