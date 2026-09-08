console.log("Remove service js loaded");

function removeService() {
    const productTypeFields = document.querySelectorAll(
        ".remove_service_product_type"
    );
    productTypeFields.forEach((field) => {
        const serviceInput = field.querySelector(
            'input[data-value="service"]'
        );
        if (serviceInput) {
            const serviceItem = serviceInput.closest(".o_radio_item");
            if (serviceItem) {
                serviceItem.remove();
                console.log("Service removed");
            }
        }
    });
}
setInterval(removeService, 500);
