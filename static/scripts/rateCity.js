//get all stars
var one = document.getElementsByName("1")
var two = document.getElementsByName("2")
var three = document.getElementsByName("3")
var four = document.getElementsByName("4")
var five = document.getElementsByName("5")

var form = document.getElementsByClassName('rate_form')
var csrf = document.getElementsByName('csrfmiddlewaretoken')


function rated(value, city) {
	for (const cityForm of form) {
		if (cityForm.id === city) {
			const children = cityForm.children;

			//if user clicks same button twice remove rating else change rating
			if (value !== 0) {
				for (const child of children) {
					child.classList.remove('rated')
				}

				for (let i = 0; i < children.length; i++) {
					if (i <= value) {
						children[i].classList.add('rated');
					} else {
						children[i].classList.remove('rated');
					}
				}
			} else {
				for (const child of children) {
					child.classList.remove('rated')
				}
			}
		}
	}
}


function handleStarSelect(size, city) {
	for (const cityForm of form) {
		if (cityForm.id === city) {
			const children = cityForm.children;

			for (let i = 0; i < children.length; i++) {
				if (size !== 0) {
					if (i <= size) {
						children[i].classList.add('checked');
					} else {
						children[i].classList.remove('checked');
					}
				} else {
					children[i].classList.remove('checked');
				}
			}
		}
	}
}


function showNotLoggedInAlert() {
	alert('You must be signed in to use this feature.');
}


function rateAttraction() {
	leaveRating(event.target.name, event.target.value);
}


function leaveRating(rating, name) {

	$.ajax({
		type: 'POST',
		url: 'rating/',
		data: {
			'csrfmiddlewaretoken': csrf[0].value,
			'name': name,
			'score': rating,
		},
		dataType: 'json',
		success: function(response) {
			rated(response.score, name);
		},
		error: function(error){
			console.log(error)
			alert("oops, something went wrong")
		}
	})
}

if (one) {
	const a = [one, two, three, four, five];

	//This makes sure the existing rating reapears when page is refreshed.
	for (const city of cit) {
		for (let i=0; i<cityRatingName.length; i++) {
			if (city === cityRatingName[i]) {
				rated(cityRatingValue[i], city);
			}
		}
	}

	for (let j=1; j<=cit.length; j++) {
		for (const star of a) {
			star[j-1].addEventListener('mouseover', function(){handleStarSelect(event.target.name, event.target.value)});
			star[j-1].addEventListener('mouseleave', function(){handleStarSelect(0, event.target.value)});
		}
	}

}