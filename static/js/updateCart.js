var updateButtons = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateButtons.length; i++) {
  updateButtons[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("ProductId: ", productId, "action:", action);
    console.log("USER:", user);
    if (user === "AnonymousUser") {
      console.log(user, "is not authenticated");
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  var url = "/profiles/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({ 'productId': productId, 'action': action })
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      location.reload();
    });
}
