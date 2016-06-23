var initialize = function(navigator) {
    $('#id_login').on('click', function(){
      navigator.id.request();
    });

    navigator.watch();
};

window.Superlists = {
    Accounts: {
        initialize: initialize
    }
};
