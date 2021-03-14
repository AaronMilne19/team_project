//get all stars
var one = document.getElementById("1")
var two = document.getElementById("2")
var three = document.getElementById("3")
var four = document.getElementById("4")
var five = document.getElementById("5")

var form = document.querySelector('.rate_form')
var csrf = document.getElementsByName('csrfmiddlewaretoken')


function handleStarSelect(size) {
	const children = form.children
	for (let i=0; i<children.length; i++) {
		if (i <= size) {
			children[i].classList.add('checked')
		} else {
			children[i].classList.remove('checked')
		}
	}
}

const handleSelect = (selection) => {
	switch(selection) {
		case "1": {
			handleStarSelect(1)
			return
		}
		case "2": {
			handleStarSelect(2)
			return
		}
		case "3": {
			handleStarSelect(3)
			return
		}
		case "4": {
			handleStarSelect(4)
			return
		}
		case "5": {
			handleStarSelect(5)
			return
		}
	}
}

function getNumericValue(stringValue) {
	var numericValue = parseInt(stringValue)
	return numericValue
}

if (one) {
	const a = [one, two, three, four, five]

	a.forEach(item => item.addEventListener('mouseover', (event) => {
		handleSelect(event.target.id)
	}))
}


function showNotLoggedInAlert() {
	alert('You must be signed in to use this feature.');
}


function rateAttraction() {

	a.forEach(item=> item.addEventListener('click', (event)=>{
		var val = event.target.id

		var isSubmit = false

		form.addEventListener('submit', e=>{
			e.preventDefault()
			if (isSubmit) {
				return
			}
			isSubmit = true
			var id = e.target.id
			var score = getNumericValue(val)

			$.ajax({
				type: 'POST',
				url: '/rating/',
				data: {
					'csrfmiddlewaretoken': csrf[0].value,
					'el_id': id,
					'val': score,
				},
				success: function(response){
					console.log(response)
					alert("Successfully rated")
				},
				error: function(error){
					console.log(error)
					alert("oops, something went wrong")
				}
			})
		})
	}))
}

