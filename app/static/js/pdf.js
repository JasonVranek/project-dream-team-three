$(function() {
    // jQuery selection for the product product dropdown
    var form = document.getElementsByName('main-form');
    var subtotal_elt = document.getElementById('subtotal');
    var total_elt = document.getElementById('total_total');
    var discount_elt = document.getElementById('discount_total')
    var main_rows = document.getElementById('details-table').getElementsByTagName("tbody")[0].getElementsByTagName("tr").length;
    // call to update on load

    updateForm();

    // function to call XHR and update county dropdown
    function updateForm() {
        var subtotal = 0;
        var total = 0;
        // for option in ['False', 'True']                                      //ADD THIS NEXT WEEK-> need to check both true and false, not just hardcode false
        for(let i = 1; i < main_rows - 1; i++){
            // Get the data from each row and compute the new row total
            try{
                var price = form[0]['price'+ i + 'False'].value;                // 'False' should be a variable thats either true or false
                var quantity = form[0]['quantity'+ i + 'False'].value;
                var discount = form[0]['discount'+ i + 'False'].value;
                // form[0]['price'+ i + 'False'].value = price.toFixed(2);
                // form[0]['quantity'+ i + 'False'].value = quantity.toFixed(2);        //add back in next week (its 5/23)
                // form[0]['discount'+ i + 'False'].value = discount.toFixed(2);
                // Remove the % sign 
                discount = discount.split('%').join('')
                // Calculate the new total price for the row
                var detail_total = price * quantity * (1 - discount/100);
                form[0]['total'+ i + 'False'].value =  detail_total.toFixed(2);

                // Update the total price
                subtotal += price * quantity
                total += detail_total;
            }
            catch(err){
                console.log(err);
            }
        }


        // Update the cummulative totals and inject the new values into the html
        subtotal_elt.innerHTML = 'subtotal: ' + subtotal.toFixed(2);
        total_elt.innerHTML = 'TOTAL (USD): ' + total.toFixed(2);
        discount_elt.innerHTML = 'discount: ' + (subtotal - total).toFixed(2);

    }

    // event listener to product dropdown change
    $('form').on('change', function() {
        updateForm();
    });
});