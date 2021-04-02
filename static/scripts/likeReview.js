function updateLikes(url){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        
            var voteFields = document.getElementsByClassName("votes");
            var idVoteFields = {};
            for (voteField of voteFields){
                idVoteFields[voteField.getAttribute("data-id")] = { 
                    'upvote':voteField.getElementsByClassName("upvote")[0], 
                    'downvote':voteField.getElementsByClassName("downvote")[0],
                    'upvotes':voteField.getElementsByClassName("upvotes")[0],
                    'downvotes':voteField.getElementsByClassName("downvotes")[0],
                    };
                console.log(idVoteFields[voteField.getAttribute("data-id")]);
            }
            var data = JSON.parse(this.responseText); 
            for (dataLine in data){
                if (data[dataLine]['like'] == 1) idVoteFields[dataLine]['upvote'].classList.add('upvoted');
                else if (data[dataLine]['like'] == -1) idVoteFields[dataLine]['downvote'].classList.add('downvoted');
                else {
                    idVoteFields[dataLine]['upvote'].classList.remove('upvoted');
                    idVoteFields[dataLine]['downvote'].classList.remove('downvoted');
                }
                idVoteFields[dataLine]['upvotes'].innerHTML = data[dataLine]['likes'];
                idVoteFields[dataLine]['downvotes'].innerHTML = data[dataLine]['dislikes'];
            }
        }
    }; 
    xhttp.open("GET", url, true);
    xhttp.send();
}


function handleLiking(){
    
}
