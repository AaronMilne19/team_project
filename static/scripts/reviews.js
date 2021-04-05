function updateReviews(urlRoot, sortBy){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var reviewsDiv = document.getElementById("reviews_feed");
            reviewsDiv.innerHTML = this.responseText;
            setUpLiking(reviewsDiv, urlRoot, sortBy);
        }
    }; 
    xhttp.open("GET", urlRoot + "reviews_feed/" + sortBy, true);
    xhttp.send();
}


function setUpLiking(reviewsDiv, urlRoot, sortBy){
    var likeButtons = reviewsDiv.getElementsByClassName("upvote");
    var dislikeButtons = reviewsDiv.getElementsByClassName("downvote");
    
    var i;
    for (i = 0; i < likeButtons.length; i++){
        let likeButton = likeButtons[i];
        let dislikeButton = dislikeButtons[i];
    
        likeButton.removeEventListener('click', handleLike);
        likeButton.addEventListener('click', function() {
            handleLike(this.getAttribute("data-id"), this, dislikeButton, urlRoot, sortBy);
        });
        dislikeButton.removeEventListener('click', handleDislike);
        dislikeButton.addEventListener('click', function() {
            handleDislike(this.getAttribute("data-id"), likeButton, this, urlRoot, sortBy);
        });
    }    
}

function handleLike(id, like, dislike, urlRoot, sortBy){
    if (like.classList.contains("upvoted")){
        modifyLike(urlRoot, id, "remove");
    }
    else {
        modifyLike(urlRoot, id, "like");
    }
    updateReviews(urlRoot, sortBy);
}
function handleDislike(id, like, dislike, urlRoot, sortBy){
    if (dislike.classList.contains("downvoted")){
        modifyLike(urlRoot, id, "remove");
    }
    else {
        modifyLike(urlRoot, id, "dislike");
    }
    updateReviews(urlRoot, sortBy);
}

function modifyLike(urlRoot, id, action){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", urlRoot + "modify_review_like/" + id + "/" + action, true);
    xhttp.send();
}



