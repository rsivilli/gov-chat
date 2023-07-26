var elements;

document.addEventListener('DOMContentLoaded', function(){
    elements = new govChat();
    window.addEventListener('scroll', function(){
        elements.test()
    });
    window.addEventListener('resize', function(){
        elements.update()
    });
})

window.addEventListener('load',function(event){

});

