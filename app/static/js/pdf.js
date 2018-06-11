$(function() {
    // jQuery selection for the product product dropdown
    var form = document.getElementsByName('main-form');
    var subtotal_elt = document.getElementById('subtotal');
    var total_elt = document.getElementById('total_total');
    var discount_elt = document.getElementById('discount_total')
    var op_total_elt = document.getElementById('optional_total')
    var main_rows = document.getElementById('details-table').getElementsByTagName("tbody")[0].getElementsByTagName("tr").length;
    // call to update on load

    updateForm();

    // function to update the subtotals and totals when unit price, quantity, and discount are modified
    function updateForm() {
        var subtotal = 0;
        var total = 0;
        var optional_total = 0;
        var options = ['False', 'True'];
        // Iterate through the required and then optional items
        for(var k = 0; k < options.length; k++){                                   
            option = options[k]; //False then True
            for(let i = 1; i < main_rows - 1; i++){
                // Get the data from each row and compute the new row total
                try{
                    var price = form[0]['price'+ i + option].value;               
                    var quantity = form[0]['quantity'+ i + option].value;
                    var discount = form[0]['discount'+ i + option].value;

                    // Remove the % sign for computations (will re-add later)
                    discount = discount.split('%').join('')

                    // Reformat the new html values to have pretty decimal points
                    form[0]['price'+ i + option].value = parseFloat(price).toFixed(2);
                    form[0]['quantity'+ i + option].value = parseFloat(quantity).toFixed(2);       
                    form[0]['discount'+ i + option].value = String('%' + parseFloat(discount).toFixed(2));

                    // Calculate the new total price for the row and modify the html
                    var detail_total = price * quantity * (1 - discount / 100);
                    form[0]['total'+ i + option].value =  detail_total.toFixed(2);

                    // Update the total price
                    if(option == 'False'){
                        // Only update the quotation subtotal and total for non-optional orders
                        subtotal += price * quantity
                        total += detail_total;
                    }
                    else{
                        optional_total += detail_total
                    }
                }
                catch(err){
                    //should catch the case where we try and read the prices of the Optional colspan
                    // console.log(err);
                    continue;
                }
            }
        }


        // Update the cummulative totals and inject the new values into the html
        if(navigator.language == 'en'){
            subtotal_elt.innerHTML = 'subtotal: $' + subtotal.toFixed(2);
            total_elt.innerHTML = 'TOTAL (USD): $' + total.toFixed(2);
            discount_elt.innerHTML = 'discount: $' + (subtotal - total).toFixed(2);
            op_total_elt.innerHTML = 'Optional items after discount (USD): $' + optional_total.toFixed(2);
        }
        else{
            subtotal_elt.innerHTML = '合計　(円）:' + subtotal.toFixed(2);
            total_elt.innerHTML = '総計（円）:' + total.toFixed(2);
            discount_elt.innerHTML = '割引 (円）:' + (subtotal - total).toFixed(2);
            op_total_elt.innerHTML = 'オプション製品の割引 (円）:' + optional_total.toFixed(2);
        }

    }

    // event listener to product dropdown change
    $('form').on('change', function() {
        updateForm();
    });

    // Add logic for signature pad here
    var wrapper = document.getElementById("signature-pad");
    var canvas = wrapper.querySelector("canvas");
    canvas.width = 500;
    // canvas.height = 100;
    var signaturePad = new SignaturePad(canvas, {
      // It's Necessary to use an opaque color when saving image as JPEG;
      // this option can be omitted if only saving as PNG or SVG
      backgroundColor: 'rgb(255, 255, 255)'
    });





});