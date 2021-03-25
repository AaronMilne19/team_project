var hearts = document.getElementsByName('heart');

var form = document.getElementsByClassName('heart_form');
var csrf = document.getElementsByName('csrfmiddlewaretoken');


for (const attraction of savedAttr) {
    saved(attraction, 1);
}

for (const heart of hearts) {
    heart.addEventListener('mouseover', function(){hoverStar(event.target.value)});
    heart.addEventListener('mouseleave', function(){hoverStar(0)})
}


function hoverStar(attraction) {
    for (const heart of hearts) {
        if (attraction === 0) {
            heart.classList.remove('highlight');
        } else if (heart.value === attraction) {
            heart.classList.add('highlight');
        }
    }
}


function saved(attraction, value) {
    for (const heart of hearts) {
        if (heart.value === attraction) {
           if (value === 0) {
                heart.classList.remove('saved');
           } else {
                heart.classList.add('saved');
           }
        }
    }
}


function saveAttraction() {
    const attractionName = event.target.value;

    $.ajax({
        type: 'POST',
        url: '/home/save/',
        data: {
            'csrfmiddlewaretoken': csrf[0].value,
            'name': attractionName,
        },
        dataType: 'json',
        success: function(response) {
            saved(attractionName, response.value);
        },
        error: function(error){
            console.log(error);
            alert('Oops, something went wrong!');
        }
    })
}


function showNotLoggedInAlert() {
    alert('You must be signed in to use this feature.');
}


