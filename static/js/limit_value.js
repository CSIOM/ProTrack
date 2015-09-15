$(document).on("input", ".self_rating_class", function() {

    $(".self_rating_class").each(function(){
        self_rating_val = $(this).val();
        if(self_rating_val < 0){
         this.value = "0";
     }
     if(self_rating_val > 200){
        this.value = "200";
    }
});
});
