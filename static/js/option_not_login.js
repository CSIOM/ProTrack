$(document).ready(function(){
    current_url = window.location.pathname;
    $('#optional').empty();
    if (current_url=='/signup/')
    {
    var a = reverse('signin', function(url) {
        html = "<li><a href='http://code.csiom.com/jasvir/project-management/issues'><button class='report-issue'>Report Issue</button></a></li> <li><a href='" + url + "'><button class=report-issue>Log In</button></a></li>";
        $("#optional").append(html);
    })
}
    else{
    var a = reverse('signup_view', function(url) {
        html = "<li><a href='http://code.csiom.com/jasvir/project-management/issues'><button class='report-issue'>Report Issue</button></a></li> <li><a href='" + url + "'><button class=report-issue>Sign Up</button></a></li>";
        $("#optional").append(html);
    })
}
});