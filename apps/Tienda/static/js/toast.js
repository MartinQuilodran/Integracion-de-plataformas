var toastButtons = document.querySelectorAll('.liveToastBtn');
      toastButtons.forEach(function(button) {
        button.addEventListener('click', function () {
          var toast = new bootstrap.Toast(document.getElementById('liveToast'));
          toast.show();
        });
      });