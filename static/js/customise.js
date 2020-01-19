$(function () {
  /*
  these method helps to select all the checkboxs in the cart page
   */

  $("input[type$='checkbox']").on('click',function () {
    if($(this).hasClass('Checked_T')){
      $(this).removeClass('Checked_T')
    }else {
      $(this).addClass('Checked_T')
    }
  })



  $('#selectAll').on("click",function(){

      var $mark = $("input[type$='checkbox']");
      if ($('#selectAll').hasClass('Checked_all_T')){
        $('#selectAll').removeClass('Checked_all_T')
      }else {
        $('#selectAll').addClass('Checked_all_T')
      }

      $mark.each(function () {
        if (($('#selectAll').hasClass('Checked_all_T'))&&(!($(this).hasClass('Checked_T')))) {
          $(this).trigger('click')
          $(this).addClass('Checked_T')
        }else if (!($('#selectAll').hasClass('Checked_all_T'))&&($(this).hasClass('Checked_T'))){
          $(this).trigger('click')
          $(this).removeClass('Checked_T')
        }

      })


    /*
      these method helps to select all the checkboxs in the cart page
      end
     */

  });

  /*
  these method helps to modify product quantity for customer
   */
  $("td[href$='modal_quantity']").on('click',function () {
    var item_quantity = $(this)
    $('#modified_item_id').val(item_quantity.attr('id'))
    $('#quantity_hover').text(item_quantity.text())
      $('#modify_btn').on('click',function () {
        if (($('#modify_quantity').val())==''){
          item_quantity.trigger(M.toast({html:'Please slect a item at least'}))
        } else {
          item_quantity.text($('#modify_quantity').val())
          $('#modify_btn').submit()
        }

  })
  })



  /*
  these method help to delete the order
   */
  $('#delete_btn').on('click',function () {
    var mark = $("input[type$='checkbox']")
    var delete_items = []
    if(mark.hasClass('Checked_T')){
      mark.each(function () {
        if (($(this).hasClass('Checked_T'))&&(!($(this).hasClass('Checked_all_T')))) {
          delete_items.push(parseInt($(this).parents('td').siblings('td').last().attr('id')))
            $('#delete_items_id').val(delete_items)
          $(this).parents('tr').remove()
        }
      })
      if ($(this).hasClass('Checked_all_T')) {
        $('#selectAll').trigger('click')
      }

    }else {
      $(this).trigger(M.toast({html: 'Please at least select a item'}))
    }
  })

  /*
  these method help to check out
   */
  $('#check_out_btn1').on('click',function () {
    var mark = $("input[type$='checkbox']")
    var total_prise = 0
      var check_list = []
    mark.each(function () {
      if (($(this).hasClass('Checked_T'))&&(!($(this).hasClass('Checked_all_T')))){
                  check_list.push(parseInt($(this).parents('td').siblings('td').last().attr('id')))

        var quantity = $(this).parents('td').siblings().last().text()
          var prise = $(this).parents('td').siblings('td:has(a)').find('a').text()
        var prise_float  = (parseFloat(prise)*parseInt(quantity))
        total_prise += prise_float
      }

    })
      $('#check_items_id').val(check_list)
      var opts = $('#areas')
      opts.on('change',function () {
          var tax = $('#areas option:selected').attr('id')
              $('#show_total_prise').text('The total prise for the selected products is : '+ (total_prise + (parseFloat(tax)*total_prise)) +' $')
              $('#total_prise').val((total_prise + (parseFloat(tax)*total_prise)))
          alert($('#total_prise').val())
      })
  })
  /*
  if the info is not filled, the check out btn 2 is in disable
   */

  /*
  after check out, remove the products had been selected
   */
  $('#check_out_btn2').on('click',function () {
    var mark = $("input[type$='checkbox']")
    var inputs = $('#modal_check_out').find('input')
    if (inputs.val()==''){
      $(this).trigger(M.toast({html: 'All info should be filled'}))
    }else {
      mark.each(function () {
        if (($(this).hasClass('Checked_T'))){
          $(this).parents('tr').remove()
        }
      })
    }

  })

    /*
  trigger the input area to upload the img
   */
  $('#upload_img_btn').on('click', function () {
    $('#upload_img_input').trigger('click');
  });

  /*
  to determine whether the selected file is img type, if it is, show the img on the website
   */
  $('#upload_img_input').on('change',function () {
    var imgFile = this.files[0];
    var reader = new FileReader();
    if (imgFile) {
      reader.readAsDataURL(imgFile);
    }
    reader.onloadend = function () {
      var img = document.getElementById('product_img');
        img.setAttribute('src', reader.result.toString());
        img.style.width = '300px';
        img.style.height = '300px';
    }

  });


});