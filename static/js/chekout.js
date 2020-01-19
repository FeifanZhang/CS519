/**
 * Created by 25384 on 2018/12/10.
 */
$(function(){
    $('#check_out_btn2').on('click',function () {
        alert('0')
        $.ajax({
          type:'get',
          data: '',
          url:'/shoppingCart/cartPage/',
          success: function(msg){
              if (msg!=''){
                  alert('2')
              }else {
                  alert('成功')
              }
          }
      })
    })
})