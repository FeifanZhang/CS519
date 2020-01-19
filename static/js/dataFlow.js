/**
 * Created by 25384 on 2018/10/11.
 */
$(function () {
  var navMail;
  var navUserPassword;
  var regUserName;
  var regMail;
  var regPassword;
  /*
  sign in
   */
  $('#signAction').on('click',function (event) {
    event.returnValue=false;
    navMail = $('#email').val();
    navUserPassword = $('#password').val();

    var signData = {'email':navMail, 'password':navUserPassword,};

    if (navUserPassword==''||navMail==''){
      $('#email').triggerHandler('M.toast({html: \'Please enter your information!\'})');
      M.toast({html: 'Please enter your information!'});
    }else {
      $.ajax({
        type : 'post',
        url : '/shoppingCart/signIn/',

        data : JSON.stringify(signData),

        success : function (msg) {
         if (msg!=''){
           alert(msg);
           $('#email').triggerHandler('M.toast({html: \'Your infomation is invalid\'})');
            M.toast({html: 'Your infomation is invalid'});
         }else {

           window.location.href='/shoppingCart/homepage/'
         }
        }
      });
    }
  });
  /*
  sign in end here
   */
  /*
  register here
   */
  $('#registerAction').on('click',function (event) {
          event.returnValue=false;
          regUserName = $('#re_username').val();
          regMail = $('#re_email').val();
          regPassword = $('#re_password').val();

              var registerData = {'email':regMail, 'password':regPassword, 'username':regUserName,};


          if (regPassword==''||regMail==''||regUserName==''){
      $('#email').triggerHandler('M.toast({html: \'Please enter your information!\'})');
      M.toast({html: 'Please enter your information!'});
    }else {
      $.ajax({
        type : 'post',
        url : '/shoppingCart/register/',

        data : JSON.stringify(registerData),

        success : function (msg) {
         if (msg!=''){
           alert(msg);
           $('#email').triggerHandler('M.toast({html: \'Your infomation is invalid\'})');
            M.toast({html: 'Your infomation is invalid'});
         }else {

           window.location.href='/shoppingCart/homepage/'
         }
        }
      });
    }
  });
  /*
  register end here
   */

  $('#check_out_btn2').on('click',function () {
      alert('1')

  })

});
